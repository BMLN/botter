import sys
from data.load import estimate_chunks
from data.iter import BatchProcessor, JsonlDataframeProcessor
from ast import literal_eval

from chatbot.instances.knowledgebases import WeaviateKB







from argparse import ArgumentParser


from logging import getLogger, basicConfig, INFO, ERROR
basicConfig(level=ERROR)
logger = getLogger()











def preproc(x):
    if x is None:
        return None
    
    if isinstance(x, str):
        return literal_eval(x)
    
    return x



def processor(data, kb):
    if not ("embedding" in data and "data" in data):
        raise KeyError(f"missing [{ str.join(", ", [_x for _x in ["embedding", "data"] if _x not in data])}]")
    

    data = data[data.columns.intersection(["id", "data", "embedding"])]
    data["id"] = data["id"].apply(preproc) if "id" in data else None
    data["data"] = data["data"].apply(preproc)
    data["embedding"] = data["embedding"].apply(preproc).apply(lambda x: x[0])
                
                
    kb.create(
        id=data["id"],
        embedding=data["embedding"],
        data=data["data"]
    )
    del data






if __name__ == "__main__":
    
    #configuration
    args = ArgumentParser("load")
    args.add_argument("--host", action="store", type=str, required=True)
    args.add_argument("--port", action="store", type=str, required=True)
    args.add_argument("--collection", action="store", type=str, required=True)
    args.add_argument("files", action="store", nargs="+", type=str)

    args.add_argument("--designated_load", action="store", type=float, default=0.25)
    args.add_argument("--designated_bytes", action="store", type=int, default=500000000)
    args.add_argument("--error_threshold", action="store", type=float, default=0.8)
    
    args = args.parse_args()






    #connection
    try:
        conn = WeaviateKB(args.host, args.port, args.collection)
        logger.info(f"initializing {args.collection}...")
    except:
        logger.error(f"couldn't connect to knowledgebase[{WeaviateKB.__name__}]")
        sys.exit(1)



    #read/write
    succesful_reads = []

    for x in args.files:

        try:
            logger.info(f"initializing from {x}...")

            BatchProcessor.process(
                x,
                lambda file:
                    JsonlDataframeProcessor.process(
                        file, 
                        processor,
                        False,
                        kb=conn
                    ),
                batch_size=estimate_chunks(x, args.designated_bytes, load=args.designated_load)
            )
            succesful_reads.append(True)


        except Exception as e:
            logger.error(f"could't read {x}: {str(e)}")
            succesful_reads.append(False)



    #cli exection code
    if succesful_reads and sum(succesful_reads) / len(succesful_reads) < args.error_threshold:
        logger.error(f"too many reads failed! ({sum(succesful_reads)}/{len(succesful_reads)})")
        sys.exit(1)
