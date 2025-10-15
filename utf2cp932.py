#!/usr/bin/env python3
import csv
import emoji
import argparse
from pathlib import Path
import os

def convert_csv(input_path: Path, output_path: Path):
    """UTF-8 CSV → cp932変換（絵文字文字列化、改行を\\nに変換、上書き保存）"""
    try:
        if output_path.exists():
            os.remove(output_path)

        with open(input_path, "r", encoding="utf-8", newline="") as infile, \
             open(output_path, "w", encoding="cp932", errors="replace", newline="") as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

            for row in reader:
                new_row = []
                for cell in row:
                    # 改行を "\n" に置換して1行化
                    cell = cell.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")
                    # 絵文字を :smile: などの文字列に変換
                    cell = emoji.demojize(cell)
                    new_row.append(cell)
                writer.writerow(new_row)

        print(f"✅ {input_path.name} → {output_path}（改行→\\n、上書き保存）")

    except Exception as e:
        print(f"❌ {input_path.name}: エラーが発生しました → {e}")

def main():
    parser = argparse.ArgumentParser(
        description="フォルダ内のCSVをcp932に変換（絵文字→文字列、改行→\\n、不正文字は?、上書き保存）"
    )
    parser.add_argument("input_dir", help="入力フォルダ（UTF-8 CSVがある）")
    parser.add_argument("output_dir", help="出力フォルダ（cp932 CSVを保存する）")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for csv_file in input_dir.glob("*.csv"):
        output_path = output_dir / csv_file.name
        convert_csv(csv_file, output_path)

    print("\n🎉 すべてのCSV変換が完了しました。")

if __name__ == "__main__":
    main()

