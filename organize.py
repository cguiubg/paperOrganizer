#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9

import os
import re
import sys 
import argparse



def createNewCategories(newCategories):
    exists = os.listdir('categories')
    regex = re.compile('^[A-Za-z]')
    for cat in newCategories:
        if not regex.search(cat):
            print('Categories must be strings of alphabetical characters.')
            sys.exit(1)
        if cat in exists:
            continue
        else:
            path = os.path.join('categories', cat)
            os.mkdir(path)
            print(f'Created category: {path}')

def createLinkInCategories(src, cats):
    if not os.path.exists(src):
        print(f'Source {src} does not exist.')
        sys.exit(1)
    if cats == None:
        path = os.path.join('categories', 'misc')
        if not os.path.exists(path):
            os.mkdir(path)
        os.symlink(os.path.abspath(src), path)
        print(f'Symlink created to {src} at: {path}')
    else:
        for cat in cats:
            path = os.path.join('categories', cat, os.path.basename(src))
            try:
                os.symlink(os.path.abspath(src), path)
                print(f'Symlink created to {src} at: {path}')
            except Exception as e:
                print(e)
                print(f'Category {cat} does not exist.' )
                continue

parser = argparse.ArgumentParser(
    description='Insert a file link into the categories file system.'
)
parser.add_argument('src', nargs='?',
                    help='File source.')
parser.add_argument('--mv', action='store_true',
                    help='If flagged move the source to files directory before running.')
parser.add_argument('--categories', nargs='+',
                    help='List of categories in the source.')
parser.add_argument('--new_categories', nargs='+',
                    help='Add new categories to the categories directory.')
parser.add_argument('--html',
                    help='Add an html link to files directory.')
parser.add_argument('--ls', action='store_true')

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if args.ls:
    for d in os.listdir('categories'):
        print(d)

if args.new_categories:
    newCats = args.new_categories
    newCats = createNewCategories(newCats)

if args.src:
    src = args.src
    categories = args.categories
    if args.mv:
        new_src = os.path.join('files', os.path.basename(src))
        os.rename(src, new_src)
        src = new_src
    elif args.html:
        new_src = os.path.join('files', src)
        with open(new_src, 'w') as f:
            f.write(f'\u001b]8;;{args.html}\u001b\\This is a link\u001b]8;;\u001b\\\n')
        src = new_src
    
    if args.categories:
        createLinkInCategories(src, categories)
