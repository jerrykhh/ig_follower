import argparse
from ig.file import CSVProcess


def main(args):
    args.action = [ action for action in args.action if str(action).replace(" ", "") != ""]
    actions: list = "".join(args.action).split("&")
    files = ["".join(file) for file in args.files]
    
    CSVProcess(actions=actions, file_paths=files, output_path=args.output).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ig_follower: CSV Processer")
    parser.add_argument("--action", type=str, required=True, help="There are merge, drop duplicate, remove followed (merge/drop_dup/rm_fol). Besides, you can use & to finish mulitpe action in same time like 'merge&drop_dup' ")
    parser.add_argument("--files", type=list, nargs="+", required=True, help="Please Enter the file paths")
    parser.add_argument("--output", type=str, default=None, help="Saved file path")
    args = parser.parse_args()
    main(args)