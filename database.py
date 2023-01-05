import dns.resolver
from pymongo import MongoClient, errors
from Player import Player
# import socket
#socket.getaddrinfo("mythotrivia.zqrt6cd.mongodb.net", 0)


dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

myconnection = "mongodb+srv://bsergiu:Ampulea111@mythotrivia.zqrt6cd.mongodb.net/test"
#myconnection = "mongodb://localhost:27017"
#myconnection = "mongodb://candrei:7OZJ4ifTY0SUWdFT@mythotrivia.zqrt6cd.mongodb.net/?retryWrites=true&w=majority"


class Database:
    def connect_to_db(self):
        try:
            self.client = MongoClient(myconnection, tls=True, tlsAllowInvalidCertificates=True)
        except errors.ServerSelectionTimeoutError as err:
            print("pymongo ERROR:", err)

    def add_question_to_collection(self, database, collection, document):
        db = self.client[database]
        collect = db[collection]
        collect.insert_one(document)

    def insert_doc_to_collection(self, database, collection, player):
        db = self.client[database]
        collect = db[collection]
        test_document = player.__dict__
        collect.insert_one(test_document)

    def insert_docs_to_collection(self, database, collection):
        db = self.client[database]
        collect = db[collection]
        first_names = ["Tim", "Sarah", "Jenn"]
        last_names = ["Rucsica", "Smith", "Bart"]
        ages = [21, 40, 23]
        docs = [{key: value for key, value in zip(["first_name", "last_name", "age"], (a, b, c))} for a, b, c in
                zip(first_names, last_names, ages)]

        collect.insert_many(docs)

    def delete_docs_from_collection(self, database, collection):
        db = self.client[database]
        collect = db[collection]
        collect.delete_many({})




def teorie():
    """
        mongoDB saleaza date nestructurate in format JSON
        Database(Collection(Documents))

        Document:
            detaliile legate de un obiect, sub forma de dictionar key:value
            fiecare document dintr-o colectie va avea un id propriu (cheie primara)
                    .inserted_id -> e campul care ne da acest id
        Collection:
            avem documentele, adica toate entries legate de o anumita colectie (cum ar fi carte-colectie si documentele repr anumite carti specifice)
            un fel de tabele
        DataBase:
            contie toate colectiile

        O baza, o colectie se poate crea imediat prin client.<nume> sau client.<baza>.<colectie>

        pentru a adauga un document intr-o colectie avem mai multe functii:
            -> <colectie>.insert_one(<document>{})
            -> <colectie>.insert_many([lista de documente])

        queries to find documents:
            -> <collection>.find({<perechi de field: value din colectia noastra>})
                    -> daca nu are parametru, o sa returneze toate documentele din colectia pe care apelam

                    -> ce returneaza ii un Cursor, care in esenta e un generator, iterator
                            -> ca sa ii accesam continutul fie putem sa iteram prin el prin for...in... sau sa facem cast la o lista
                    -> pe langa parametrul de query ii mai putem da si un parametru de columns
                            -> parametrul asta specifica exact ce coloane din document ne-ar interesa
                                -> 1 ne intereseaza , 0 nu ne intereseaza

                    -> putem sa cautam un document si dupa id-ul lui
                            -> pentru asta avem nevoie ca id-ul sa fie de tip bson, acelasi cu cel returnat de .inserted_id / cel stocat automat
                            -> from bson.objectid import ObjectId
                            -> _id = ObjectId(person_id)
                            -> dezavantajul e ca trebuie sa stim de dinainte id-ul

            -> <collection>.find_one({<perechi de field: value din colectia noastra>}
                    -> daca sunt mai multe perechi toate trebuie sa dea match ca sa avem return la ceva
                    -> spre deosebire de .find() care o sa returneze toate documentele care respecta query-ul, .find_one() va returna doar primul

            -> <collection>.count_documents(filter={aici putem adauga iar perechi field:value, sa filtram count-ul}


        update document:
            -> <colleciton>.update_one({"_id" : _id}, <query cu ce updates vrem sa facem>)


        replacing a document:
            ai vrea sa faci un replace atunci cand schimbi toate fields dar vrei sa ramai cu acelasi _id
            -> <collection>.replace_one("_id" : _id}, <document nou>"}

        deleting a document:
            -> <collection>.delete_one({"_id": _id})
            -> <collection>.delete_many({})


        Relatii intre documente:
            -> embedded documents: putem avea drept field intr-un document, un alt document sau chiar o lista de documente
            -> daca cele doua documente se afla in colectii diferite
                -> avem nevoie de a foreign key care sa le lege colectiile intre ele
                    -> adica in unul din documente vom avea un field care are valoare id-ul documentului cu care relationeaza




        special operators in mongo
            -> {"$and": [accepta o lista de queries, intre ele fiind relatia de si logic]} -- asta ar fi un query
            !!! pentru cele de mai jos putem da mai multe queries ce vrem sa fie modificate, ele fiind separate prin , !!!
            -> {"$set": {creeaza un nou field cu valoarea data de noi, putem sa si suprascriem un field existent}}
            -> {"$inc": {incrementeaza field-ul cu o valoare data, ma gandesc ca doar daca e int sau float}}
            -> {"$rename": {"nume vechi": "nume nou"}}
            -> {"$unset": {"<field ce vrem sa fie sters": "are nevoie de o val, poate sa fie si string gol"}}
            -> {"$addToSet" : { <field ce va fi un set/array': valoare}}
                    -> daca field-ul nu exista, el va fi creat si va contien doar valoarea adaugata
                    -> daca exista deja, valoarea va fi appenduita

    """


if __name__ == "__main__":
    myDB = Database()
    myDB.connect_to_db()
    dbs = myDB.client.list_database_names() #obtinem o lista cu toate bazele de date din mongodb asociate cu ip-ul

    test_db = myDB.client.test# metoda de a accesa una dintre colectii, mai avem si varianta dictionar cu client["test"]

    collections = test_db.list_collection_names()
    player = Player("andrei", "test", "email")
    myDB.insert_doc_to_collection("test", "test", player)
    myDB.insert_docs_to_collection("test", "test")
    myDB.delete_docs_from_collection("test", "test")
    smth = {
        "question": "Who are considered the big three in Greek Myth?",
        "answers": ("Zeus, Hades, Poseidon", "Hera, Poseidon, Demeter", "Zeus, Hades, Athena", "Zeus, Poseidon, Hermes"),
        "correct_answer": "Zeus, Hades, Poseidon",
        "points": 5
    }
    smth1 = {
        "question": "Who are considered the big three in Roman Myth?",
        "answers": ("Zeus, Hades, Poseidon", "Hera, Poseidon, Demeter", "Zeus, Hades, Athena", "Zeus, Poseidon, Hermes"),
        "correct_answer": "Zeus, Hades, Poseidon",
        "points": 5
    }
    smth2 = {
        "question": "Who are considered the big three in Nordic Myth?",
        "answers": ("Thor, Loki, Odin", "Odin, Poseidon, Frey", "Zeus, Freya, Athena", "Zeus, Poseidon, Hermes"),
        "correct_answer": "Zeus, Hades, Poseidon",
        "points": 5
    }
    # myDB.add_question_to_collection("test", "questions", smth)
    myDB.add_question_to_collection("test", "questions", smth2)
    print(smth["answers"][2])
