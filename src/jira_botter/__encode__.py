import sys
from os import path, mkdir
from tempfile import TemporaryDirectory
from shutil import copy, rmtree

import pandas as pd
from data.load import estimate_chunks
from data.iter import BatchProcessor, CsvDataframeProcessor

from chatbot.instances.vectorizers import HFVectorizer




from argparse import ArgumentParser

















if __name__ == "__main__":

    args = ArgumentParser("encode")
    args.add_argument("--encoder_model", action="store", type=str, default="Qwen/Qwen3-Embedding-4B")
    args.add_argument("--input", action="store", type=path.abspath, required=True)
    args.add_argument("--output", action="store", type=path.abspath, default="./data.json")
    args.add_argument("--text_column", action="store", type=str, required=True)
    args.add_argument("--data_columns", action="store", nargs="+", type=str, default=[])
    args.add_argument("--designated_load", action="store", type=float, default=0.25)
    args.add_argument("--designated_bytes", action="store", type=int, default=500000000)

    args = args.parse_args()


    if not path.isfile(args.input):
        print("input isnt a file")
        sys.exit(1)
    
    if path.isfile(args.output):
        print("output file already exists")
        sys.exit(1)




    try:
        encoder = HFVectorizer(args.encoder_model)
        def process_df(df):
            if not args.text_column in df:
                raise ValueError(f"text_column ({args.text_column}) is invalid for inputdata {args.input} ({df.columns.tolist()})")
                
            if not all((x in df for x in args.data_columns)):
                raise ValueError(f"data_columns ({[x for x in args.data_columns if not x in df]}) are invalid for inputdata {args.input} ({df.columns.tolist()})")


            text = df[args.text_column]
            data = pd.Series(df[args.data_columns if args.data_columns else df.columns].to_dict(orient="records") or [ {} ] * len(df))
            del df
            
            data = pd.DataFrame(
                {
                    "embeddings": encoder.vectorize(text.tolist()),
                    "data": data
                }
            )
            data.to_json(args.output, mode="a", lines=True, orient="records")

            del text
            del data



        if not path.isdir("./.processing"):
            mkdir("./.processing")

        if not path.isdir(proc_dir := path.join("./.processing", path.basename(args.input).split(".")[0])):
            mkdir(proc_dir)
            
        with TemporaryDirectory(dir=proc_dir, delete=False) as td:
            copy(args.input, inp := path.join(td, path.basename(args.input)))

            BatchProcessor.process(
                inp, 
                lambda file: 
                    CsvDataframeProcessor.process(
                        file, 
                        process_df,
                        False
                    ),
                batch_size=estimate_chunks(args.input, args.designated_bytes, load=args.designated_load)
            )
        
        rmtree(td)



    except Exception as e:
        print(f"Failed: {e}")

        sys.exit(1)