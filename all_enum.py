from enum import Enum


class Answer(Enum):
    READY = "I'm ready !"
    PONG = "Pong"
    OK = "OK"

    CMD_MUST_CONNECT_BEFORE = "Vous devez vous connecter avant de poursuivre"
    CMD_MY_Id = "# Discord ne demandera jamais vos identifiants MYGES !"
    CMD_MY_TUTO = "## Pour vous connectez, saisissez: \n!login *identifiant* *mot de passe*\n*> Vous aurez accès au " \
                  "bot pendant 5 min*"
    CMD_WARNING_PARAM = "## Vous devez renseigner 2 paramètres"
    CMD_NOT_AUTHORIZED = "Vous n'avez pas les autorisations nécessaires pour créer des canaux."
    CMD_CANNOT_EXEC = "## Vous ne pouvez pas executer cette commande dans ce channel"
    CMD_DONE = "Bien t’as tout scrapé bg"
    CMD_NOT_FOUND = "La commande n'existe pas !"
    CMD_ERROR = "La commande a rencontré une erreur !"


class Filename(Enum):
    FOLDER_SYLLABUS = "ScrapSyllabus/"
    FILE_SYLLABUS = "_syllabus_semester_"

    FOLDER_MARK = "ScrapMark/"
    FILE_MARK = "_marks_semester_"

    FOLDER_STUDENT = "ScrapStudents/"
    FILE_STUDENT = "_students"

    FOLDER_PLANNING = "ScrapPlanning/"
    FILE_PLANNING = "_planning"

    def get_filename(self, username, semester):
        return f"{username}{self.value}{semester}.json"
