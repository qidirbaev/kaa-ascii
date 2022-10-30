import pdfplumber
import timeit
import json

WORD_COUNTER = 0
BOTTOM = 14
TOP = 510


def parser(path, from_page, to_page):
    word_dicts = []

    with pdfplumber.open(path) as pdf:
        for i in range(from_page, to_page):
            try:
                text = pdf.pages[i]
                words = text.extract_words()

                for word in words[2: len(words) - 1]:
                    text = str(word["text"].strip())

                    left = text[0]
                    right = text[len(text) - 1]

                    if not left.isalpha() or right.endswith(".") or len(text) < 3:
                        continue

                    if right == ",":
                        word_dicts.append({
                            "word": text[:-1]
                        })
                    else:
                        word_dicts.append({
                            "word": text
                        })

                    global WORD_COUNTER
                    WORD_COUNTER += 1
            except:
                print('PageError at #', i)
                break
        return word_dicts


def write_file(name, obj):
    try:
        json_obj = json.dumps(obj, indent=4)
        with open(f"{name}.json", "w") as outfile:
            outfile.write(json_obj)
    except Exception as err:
        print("WriteFileError", err)


if __name__ == '__main__':
    try:
        start_time = timeit.default_timer()
        doc = parser("assets/qq-orfo-sozlik.PDF", BOTTOM, TOP)
        write_file(f"kaa-ascii-words_{BOTTOM}-{TOP}", doc)
        end_time = timeit.default_timer()

        delta = end_time - start_time

        print(f"Operation takes ~{round(delta * 1000)}ms for parse {WORD_COUNTER} words")

    except Exception as e:
        print("OperationError", e)
