import argparse
from .io import read_from_file, write_to_file
from .translators import get_translator


parser = argparse.ArgumentParser(
    description="Translate english into morse or vice versa"
)
parser.add_argument("-t", "--target-lang", type=str, default="morse",
                    help="output file language")
parser.add_argument("-s", "--source-lang", type=str, default="english",
                    help="input file language")
parser.add_argument("output_file", type=str,
                    help="path to output file")
parser.add_argument("input_file", type=str,
                    help="path to input file")

args = parser.parse_args()
if args.source_lang == "morse" and args.target_lang == "morse":
    args.target_lang = "english"

try:
    translator = get_translator(args.source_lang, args.target_lang)
    input_string = read_from_file(args.input_file)
    output_string = translator.translate(input_string)
    write_to_file(output_string, args.output_file)
except Exception as e:
    print(f'Error in translation: {str(e)}')
