import spacy

nlp = spacy.load("en_core_web_sm")


def find_persons(text):
    doc = nlp(text)

    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    # Return persons
    return persons


if __name__ == "__main__":
    text = "John and Mary went to the park. Peter met them there."

    # Find persons in the text
    persons = find_persons(text)

    # Print the found persons
    print("Persons found:")
    for person in persons:
        print(person)
