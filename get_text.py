import conllu
import csv
import urllib.request

def make_link(file, sheet):
    return f'https://docs.google.com/spreadsheets/d/{file}/export?format=csv&id={file}&gid={sheet}'

csvs = {
    'girnar': ('1HuNs_AnkII5eQFozIX3q-dlQEGSLOw_nq3mfLZY3Rpw', [
        '0', '1786988864'
    ])
}

result = ""

# go through all the csvs
for location in csvs:
    file = csvs[location][0]
    for num, edict in enumerate(csvs[location][1]):
        link = make_link(file, edict)

        # download all the csvs and store with nice names
        name = f'not-to-release/csv/{location}-{num + 1}.csv'
        urllib.request.urlretrieve(link, name)

        # go through csv and cleanup
        with open(name, 'r') as fin:
            reader = csv.reader(fin)
            txt = ""
            ct = 1

            # each row of csv
            for i, row in enumerate(reader):

                # ignore header
                if i == 0: continue
                # print(row)
                # input()

                row = row[:10]

                # sort feats (split string into list separated by |, sort, then rejoin with |)
                row[5] = '|'.join(sorted(row[5].split('|')))
                row[9] = '|'.join(sorted(row[9].split('|')))

                # add sentence ids when at new sentence (+ ignore non-initial cell)
                if row[0].startswith('text = '):
                    row[0] = "# " + row[0]
                    row = [row[0]]
                    txt += f'# sent_id = {location}-{num + 1}-{ct}\n'
                    ct += 1
                # empty row means ignore all cells
                elif row[0] == '':
                    row = []
                
                # cleanup: remove whitespace on either side, _ in empty cells
                row = [x.strip() for x in row]
                row = [x if x else '_' for x in row]

                # conllu-ize and add to string
                txt += '\t'.join(row) + '\n'

            # add string to final output
            result += txt

# write final output
with open('pra_dipi-ud-train.conllu', 'w') as fout:
    fout.write(result)
