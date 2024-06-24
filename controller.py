import time
import flet as ft
import model as md

class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view

    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")


    def handleSpellCheck(self):
        tipo = self._view._mode_dd.value
        lingua = self._view._language_dd.value
        testo = self._view._sentence_tf.value

        print(tipo)
        print(lingua)
        print(testo)
        continua = True
        if lingua is None:
            self._view._output_lv.controls.append(ft.Text(f"Language must be selected"))
            continua = False
        if tipo is None:
            self._view._output_lv.controls.append(ft.Text(f"Modality must be selected"))
            continua = False
        if testo.__eq__(""):
            self._view._output_lv.controls.append(ft.Text(f"Sentence cannot be empty"))
            continua = False
        if continua is False:
            self._view.update()
            return

        self._view._output_lv.controls.clear()

        parole, tempo = self.handleSentence(testo, lingua, tipo)
        self._view._output_lv.controls.append(ft.Text(f"1: Initial sentence: {testo}"))
        self._view._output_lv.controls.append(ft.Text(f"2: Errors: {parole}"))
        self._view._output_lv.controls.append(ft.Text(f"3: Time: {str(tempo)}"))
        self._view._sentence_tf.value = ""

        self._view.update()

    def handle_language_dd_changed(self, e):
        if self._view._language_dd.value is None:
            return
        self._view._output_lv.controls.append(ft.Text(f"Language {self._view._language_dd.value} successfully selected"))
        self._view._output_lv.update()

    def handle_mode_dd_changed(self, e):
        if self._view._mode_dd.value is None:
            return
        self._view._output_lv.controls.append(ft.Text(f"Modality {self._view._mode_dd.value} successfully selected"))
        self._view._output_lv.update()


def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text