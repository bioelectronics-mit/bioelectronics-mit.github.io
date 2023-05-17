# 2023-05-17
# Python code to import unupdated publications since 2022-1-1

import os
import re
import bibtexparser
from crossref.restful import Works

def save_entry_to_bib(entry, directory):
    with open(os.path.join(directory, 'cite.bib'), 'w') as f:
        db = bibtexparser.bibdatabase.BibDatabase()
        db.entries = [entry]
        f.write(bibtexparser.dumps(db))

def get_authors(paper):
  num_author = len(paper['author'])
  authors = []
  for i in range(0, num_author):
    author = paper['author'][i]['family'] + ', ' + paper['author'][i]['given']
    authors.append(author)
  return authors

def load_abst(paper):
  try:
    abst = paper['abstract']
    abst = re.split('[ <>]', abst)
    abst = [i for i in abst if 'jats' not in i and len(i) != 0]
    abst = abst[1:]
    abst = ' '.join(abst)
    return abst
  except:
    print('"abstract" does not exist')

def save_entry_to_index(entry, directory):
    with open(os.path.join(directory, 'index.md'), 'w') as f:
      works = Works()
      doi = entry['doi']
      print(doi)
      url = 'https://doi.org/' + doi
      paper = works.doi(url)

      load_abst(paper)

      authors = get_authors(paper)
      title = paper['title']
      title = ' '.join(title)
      journal = paper['container-title']
      journal = ' '.join(journal)
      date = paper['created']['date-parts'][0]
      datetime = paper['created']['date-time']

      try:
        volume = paper['volume']
        number = paper['issue'] #test later
        issn = paper['issn-type'][0]['value']
      except:
        print('no volume, number, or issn')

      abstract = load_abst(paper)

      doi = doi
      url = url

      f.write('---\n')
      f.write('title: "' + title + '"\n')
      f.write('date: ' + str(date) + '\n')
      f.write('publishDate: ' + datetime + '\n')
      f.write('authors: [')
      for i in range(0, len(authors)-1):
        a = authors[i].split(', ')
        f.write('"'+a[1]+' '+a[0]+'", ')
      a = authors[-1].split(' ,')
      f.write('"'+a[1]+' '+a[0]+'"]\n')
      f.write('publication_types: ["2"]\n')
      f.write('featured: false\n')
      f.write('publication: "*' + journal + '*"\n\n')
      
      f.write('doi: "' + url + '"\n')
      try:
        f.write('abstract: "' + abstract + '"\n\n')
      except:
        f.write('abstract: "' +  '"\n\n')
        print('no abstract')
      f.write('---')


def get_id(entry):
    id = re.split('\d+', entry['ID'])
    year = re.split('\D+', entry['ID'])
    id = id[0] + '-' + year[1] + '-' + id[1]
    return id

def create_directory_based_on_entry(entry, parent_directory):
    id = get_id(entry)
    directory_path = os.path.join(parent_directory, id)
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

def process_bib_file(file_path, parent_directory):
    with open(file_path, 'r') as f:
        bib_database = bibtexparser.load(f)

    for entry in bib_database.entries:
        dir_path = create_directory_based_on_entry(entry, parent_directory)
        save_entry_to_bib(entry, dir_path)
        # try:
        save_entry_to_index(entry, dir_path)
        # except:
        #   print(f'error in {entry}')

def make_citebib(entry, directory):
  with open(os.path.join(directory, 'cite.bib'), 'w') as f:
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [entry]
    f.write(bibtexparser.dumps(db))

# Call the function to process the bib file
process_bib_file('Anikeeva-GoogleScholar-BibTex-2023-05-14.bib', 'test3')
