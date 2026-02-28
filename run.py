from typing import Generator, Iterable
from tagger.interrogator import Interrogator
from PIL import Image
from pathlib import Path
import argparse
import sys
from tagger.interrogators import interrogators

filename = ""
i = 1
flag_pos = 0
f = False
"""
for ii in range(1, len(sys.argv)):
    if sys.argv[i] == "--file":
        f = True
        flag_pos = i + 1
    if f:
        if sys.argv[i] != "--file":
            filename = filename + sys.argv[i]
            sys.argv[i] = ""
    i += 1

sys.argv[flag_pos] = filename
#print(sys.argv)
"""
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dir', help='ディレクトリ内の全画像の予測')
group.add_argument('--file', help='1ファイルの予測')
#group.add_argument('--threshold', type=float,default=0.1,help='予測の閾値')

parser.add_argument(
    '--threshold',
    type=float,
    default=0.35,
    help='予測の閾値（デフォルトは0.35）'
)

parser.add_argument(
    '--model',
    default='wd14-convnextv2.v1',
    choices=list(interrogators.keys()),
    help='予測に使用するモデル名（デフォルトはwd14-convnextv2.v1）'
)

#args = parser.parse_args()

parser.add_argument(
    '--ext',
    default='.txt',
    help='ディレクトリオプションの場合、キャプションファイルに追加する拡張子（デフォルトは.txt）'
)
parser.add_argument(
    '--overwrite',
    action='store_true',
    help='キャプションファイルが存在する場合に上書きする'
)
parser.add_argument(
    '--cpu',
    action='store_true',
    help='CPUのみ使用'
)
parser.add_argument(
    '--rawtag',
    action='store_true',
    help='モデルの生の出力を使用'
)
parser.add_argument(
    '--recursive',
    action='store_true',
    help='再帰的にファイル検索を有効にする'
)
parser.add_argument(
    '--exclude-tag',
    dest='exclude_tags',
    action='append',
    metavar='t1,t2,t3',
    help='除外するタグを指定（カンマ区切りリスト）'
)

args = parser.parse_args()
print(args.file)
print("*****************************")
# interrogator設定を取得
interrogator = interrogators[args.model]

if args.cpu:
    interrogator.use_cpu()

def parse_exclude_tags() -> set[str]:
    if args.exclude_tags is None:
        return set()

    tags = []
    for str in args.exclude_tags:
        for tag in str.split(','):
            tags.append(tag.strip())

    # 逆エスケープ（naiタグをdanbooruタグに変換）
    reverse_escaped_tags = []
    for tag in tags:
        tag = tag.replace(' ', '_').replace('\(', '(').replace('\)', ')').replace('censored', '').replace('bar censor', '').replace('monochrome', '').replace('greyscale', '')
        reverse_escaped_tags.append(tag)
    return set([*tags, *reverse_escaped_tags])  # 重複を削減

def image_interrogate(image_path: Path, tag_escape: bool, exclude_tags: Iterable[str]) -> dict[str, float]:
    """
    画像パスからの予測
    """
    im = Image.open(image_path)
    result = interrogator.interrogate(im)

    return Interrogator.postprocess_tags(
        result[1],
        threshold=args.threshold,
        escape_tag=tag_escape,
        replace_underscore=tag_escape,
        exclude_tags=exclude_tags)

def explore_image_files(folder_path: Path) -> Generator[Path, None, None]:
    """
    フォルダパスを探索して画像ファイルを取得
    """
    for path in folder_path.iterdir():
        if path.is_file() and path.suffix in ['.png', '.jpg', '.jpeg', '.webp']:
            yield path
        elif args.recursive and path.is_dir():
            yield from explore_image_files(path)

if args.dir:
    root_path = Path(args.dir)
    for image_path in explore_image_files(root_path):
        caption_path = image_path.parent / f'{image_path.stem}{args.ext}'

        if caption_path.is_file() and not args.overwrite:
            # キャプションが存在する場合はスキップ
            print('スキップ:', image_path)
            continue

        print('処理中:', image_path)
        tags = image_interrogate(image_path, not args.rawtag, parse_exclude_tags())

        tags_str = ', '.join(tags.keys())

        with open(caption_path, 'w', encoding='utf-8') as fp:
            fp.write(tags_str)

if args.file:
    tags = image_interrogate(Path(args.file).resolve(), not args.rawtag, parse_exclude_tags())
    tags_str = ', '.join(tags.keys())
    print("\n" + tags_str.replace('censored,', '').replace('bar censor,', '').replace('monochrome,', '').replace('greyscale,', '').replace('mosaic censoring,', '').replace('pointless censoring,', '').replace('heart censor,', ''))



