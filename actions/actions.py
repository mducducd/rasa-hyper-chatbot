# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
# from underthesea import pos_tag
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.vietnamese_correction import *
import random
import string
import mysql.connector
from rasa_sdk import Tracker, FormValidationAction
from datetime import datetime

mydb = mysql.connector.connect(host="localhost", user="root", database="rasa_hyper")
mycursor = mydb.cursor()

def DataUpdate(cust_name,cust_cmnd,account_number):
    # sql = 'CREATE TABLE accounts (name VARCHAR(255), cmnd VARCHAR(255) , account_number VARCHAR(255),balance INT)'
    balance = 10000000;
    sql='INSERT INTO accounts (full_name, id_card, account_number,balance) VALUES ("{0}","{1}", "{2}","{3}");'.format(cust_name,cust_cmnd,account_number,balance)
    mycursor.execute(sql)
    mydb.commit()

def getServiceName():
    # sql = 'CREATE TABLE accounts (name VARCHAR(255), cmnd VARCHAR(255) , account_number VARCHAR(255),balance INT)'
    sql='select service from services'
    mycursor.execute(sql)
    result = mycursor.fetchall();
    mydb.commit()
    return result

def addServiceName(s):
    sql = 'INSERT INTO services (service) VALUES ("{}");'.format(s)
    mycursor.execute(sql)
    mydb.commit()

def CheckExist(cust_name,cust_cmnd,account_number):
    sql='select COUNT(*) from accounts where full_name = "{0}" and id_card = "{1}" and account_number = "{2}";'.format(cust_name,cust_cmnd,account_number)
    mycursor.execute(sql)
    count = mycursor.fetchone()
    print(count[0])
    mydb.commit()
    return count[0]

def CheckAccountExist(cust_name,cust_cmnd):
    sql='select COUNT(*) from accounts where full_name = "{0}" and id_card = "{1}";'.format(cust_name,cust_cmnd)
    mycursor.execute(sql)
    count = mycursor.fetchone()
    print(count[0])
    mydb.commit()
    return count[0]

def CheckBalance(cust_name,cust_cmnd,account_number):
    sql='select balance from accounts where full_name = "{0}" and id_card = "{1}" and account_number = "{2}";'.format(cust_name,cust_cmnd,account_number)
    print(sql)
    mycursor.execute(sql)
    balance = mycursor.fetchone()
    mydb.commit()
    return balance[0]

def getBalance(account_number):
    mycursor = mydb.cursor()
    sql='select balance from accounts where account_number={}'.format(account_number)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult[0][0]

# S???a ch??nh t??? cho t??n
def NameCorrect(s):
    s = chuan_hoa_dau_cau_tieng_viet(s)
    return  string.capwords(s)

def numOfAccounts():
    mycursor = mydb.cursor()
    sql='select count(*) from accounts '
    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    return myresult[0]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        count = CheckExist(tracker.get_slot('name'), tracker.get_slot('cmnd'),
                           tracker.get_slot('cust_account_number'))
        if count >= 1:
            return [SlotSet("login", 'true')]
        else:
            return [SlotSet("login", 'false')]

class ActionCreateAccount(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_create_account"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = (
            "M???i qu?? kh??ch x??c nh???n th??ng tin.  T??n : {0} /n S??? cmnd : {1} /n Qu?? kh??ch c?? mu???n ti???p t???c kh??ng ?"
                .format(tracker.get_slot("cust_name"), tracker.get_slot("cust_cmnd"))
        )
        buttons = [
            {"payload": "/affirm", "title": "C??"},
            {"payload": "/deny", "title": "kh??ng"},
        ]

        dispatcher.utter_message(text=text, buttons=buttons)
        return []

account_number = 0

class ActionCreateAccountSubmit(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_create_account_submit"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # account_number = random.randint(100000000000, 999999999999);
        account_number = 100000000000 + numOfAccounts()

        DataUpdate(tracker.get_slot("name"),
                   tracker.get_slot("cmnd"),account_number)
        dispatcher.utter_message("{} ???? t???o t??i kho???n th??nh c??ng".format(tracker.get_slot("cust_sex")))
        dispatcher.utter_message("S??? t??i kho???n c???a b???n l?? {}".format(account_number))
        cust_name = tracker.get_slot("name")
        print(cust_name)
        cust_name = list(cust_name.split(" "))
        # return_slots = []
        # return_slots.append(SlotSet("cust_name", tracker.get_slot('name')))
        # return_slots.append(SlotSet("cust_cmnd", tracker.get_slot('cmnd')))
        # return_slots.append(SlotSet("cust_account_number", account_number))
        # print(tracker.get_slot('cust_name'))
        # print(tracker.get_slot('cmnd'))
        # print(tracker.get_slot('cust_account_number'))

        if tracker.get_slot("cust_sex") != "Qu?? kh??ch":
            if cust_name[-1].lower != "anh":
                return[SlotSet("cust_name", tracker.get_slot('name')),
                       SlotSet("cust_cmnd", tracker.get_slot('cmnd')),
                       SlotSet("cust_account_number", account_number),
                       SlotSet("cust_sex",tracker.get_slot("cust_sex") + " " + cust_name[-1])]
            else:
                return [SlotSet("cust_name", tracker.get_slot('name')),
                        SlotSet("cust_cmnd", tracker.get_slot('cmnd')),
                        SlotSet("cust_account_number", account_number),
                        SlotSet("cust_sex", tracker.get_slot("cust_sex") + " " + cust_name[-2:])]
        else:
            return [SlotSet("cust_name", tracker.get_slot('name')),
                    SlotSet("cust_cmnd", tracker.get_slot('cmnd')),
                    SlotSet("cust_account_number", account_number),
                    SlotSet("cust_sex", tracker.get_slot("cust_sex"))]


class ActionCreateAccountForOthersPesonSubmit(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_create_account_for_others_person_submit"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # account_number = random.randint(100000000000, 999999999999)
        account_number = 100000000000 + numOfAccounts()
        DataUpdate(tracker.get_slot("name"),
                   tracker.get_slot("cmnd"),account_number)
        text = (
            "Qu?? kh??ch c?? mu???n ti???p t???c kh??ng ?"
        )
        buttons = [
            {"payload": "/affirm", "title": "Yes"},
            {"payload": "/deny", "title": "No"},
        ]

        dispatcher.utter_message(text=text, buttons=buttons)
        dispatcher.utter_message("Qu?? kh??ch ???? t???o t??i kho???n cho {} th??nh c??ng".format(tracker.get_slot("others_person_sex")))
        dispatcher.utter_message("Your account number is {}".format(account_number))
        return []

class ActionListServiceName(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_list_service_name"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        list_service = getServiceName()
        # print(list_service)
        text = (
            "G???i qu?? kh??ch danh s??ch d???ch v???:"
        )
        count = 0;
        buttons = []
        for row in list_service:
            intent = ''
            if row[0] == 'Xem s??? d?? t??i kho???n':
                intent = 'check_balance_account'
            elif row[0] == '????ng k?? t??i kho???n':
                intent = 'create_account'
            elif row[0] == 'Xem kho???n vay t???i ??a':
                intent = 'check_loan_max'
            elif row[0] == '????ng nh???p t??i kho???n':
                intent = 'cust_sign_in'
            count = count + 1
            buttons.append({"payload": f"/{intent}", "title": f"{row[0]}"})
        dispatcher.utter_message(text=text, buttons=buttons)
        return []

import requests

class ActionExchangeRate(Action):
    def name(self) -> Text:
        return "action_exchange_rate"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # url = str.__add__('http://data.fixer.io/api/latest?access_key=', 'AWPO998N8W05HK1K')
        # c = Currency_convertor(url);
        dola = ['????','???? la','???? la m???','usd','$']
        bang = ['b???ng','b???ng anh','gbp']
        yen = ['y??n','y??n nh???t','jpy']
        ndt = ['nh??n d??n t???','cny']
        eur = ['eur','euro','???']
        vnd = ['ti???n vi???t','vnd','vn??', '?????ng', 'dong']
        from_country = tracker.get_slot('currency_from')
        to_country = tracker.get_slot('currency_to')
        # from_country = next(from_country)
        # to_country = next(to_country)
        print(from_country)
        if from_country == None:
            dispatcher.utter_message(text=f'Xin l???i, t??i kh??ng t??m th???y t??? gi?? ')
            return []
        else:
            if from_country.lower() in dola:
                from_country = 'usd'
            elif from_country.lower() in bang:
                from_country = 'gbp'
            elif from_country.lower() in yen:
                from_country = 'jpy'
            elif from_country.lower() in ndt:
                from_country = 'cny'
            elif from_country.lower() in eur:
                from_country = 'eur'
            elif from_country.lower() in vnd:
                from_country = 'vnd'
            else:
                dispatcher.utter_message(text=f'Xin l???i, t??i kh??ng t??m th???y t??? gi?? n??y')
                return []
        if to_country == None:
            to_country = 'vnd'
        else:
            if to_country.lower() in dola:
                to_country = 'usd'
            elif to_country.lower() in bang:
                to_country = 'gbp'
            elif to_country.lower() in yen:
                to_country = 'jpy'
            elif to_country.lower() in ndt:
                to_country = 'cny'
            elif to_country.lower() in eur:
                to_country = 'eur'
            elif to_country.lower() in vnd:
                to_country = 'vnd'
            else:
                dispatcher.utter_message(text=f'Xin l???i, t??i kh??ng t??m th???y t??? gi?? n??y')
                return []
        amount = tracker.get_latest_entity_values(entity_type="number");
        amount = next(amount)
        if (amount == None):
            amount = 1
        # Where USD is the base currency you want to use
        key = '{}_{}'.format(from_country.upper(), to_country.upper())
        url = 'https://free.currconv.com/api/v7/convert?q={}&compact=ultra&apiKey=cd5587fe0a7e2606551b'.format(key)

        # # Making our request
        # print(to_country.upper())
        response = requests.get(url)
        data = response.json()

        # rate = data['conversion_rates'][to_country.upper()]
        dispatcher.utter_message(text=f'{amount} {from_country.upper()} = {data[key]} {to_country.upper()}')
        return[SlotSet("currency_to", 'vnd')]

class ActiobSetName(Action):

    def name(self):
        return "action_set_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("cust_name", tracker.get_slot('name'))]


class ActiobSetCmnd(Action):

    def name(self):
        return "action_set_cmnd"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("cust_cmnd", tracker.get_slot('cmnd'))]

class ActiobSetAccountNumber(Action):

    def name(self):
        return "action_set_account_number"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("cust_account_number", account_number)]

class ActiobResetName(Action):

    def name(self):
        return "action_reset_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('cust_name'))
        print(tracker.get_slot('cust_cmnd'))
        print(tracker.get_slot('cust_account_number'))
        return [SlotSet("name", None)]

class ActiobResetCmnd(Action):

    def name(self):
        return "action_reset_cmnd"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("cmnd", None)]


class ActionCheckBalance(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f's??? d?? t??i kho???n c???a qu?? kh??ch l?? {CheckBalance(tracker.get_slot("cust_name"),tracker.get_slot("cust_cmnd"),tracker.get_slot("cust_account_number"))}')
        return[]

class ActionCheckLoanMax(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_check_loan_max"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        balance = CheckBalance(tracker.get_slot("cust_name"),tracker.get_slot("cust_cmnd"),tracker.get_slot("cust_account_number"))
        loan_max = balance + balance * 0.6
        dispatcher.utter_message(text=f'kho???n vay t???i ??a c???a qu?? kh??ch l?? {loan_max}')
        return[]

class ActionCheckLogin(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_check_login"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('cust_name'))
        print(tracker.get_slot('cust_cmnd'))
        print(tracker.get_slot('cust_account_number'))
        if tracker.get_slot('cust_name') == None and tracker.get_slot('cust_cmnd') == None and tracker.get_slot('cust_account_number') == None:
            return [SlotSet("login", 'false')]
        else:
            count = CheckExist(tracker.get_slot('cust_name').lower(),tracker.get_slot('cust_cmnd'),tracker.get_slot('cust_account_number'))
            if count >= 1:
                return [SlotSet("login", 'true')]
            else:
                return [SlotSet("login", 'false')]

class ActionCheckAccount(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_check_account"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('name') == None and tracker.get_slot('cmnd') == None :
            return [SlotSet("account", 'false')]
        else:
            count = CheckAccountExist(tracker.get_slot('name').lower(),tracker.get_slot('cmnd'))
            if count >= 1:
                return [SlotSet("account", 'true')]
            else:
                return [SlotSet("account", 'false')]

class ValidateCustCreateAccount(FormValidationAction):
    def name(self) -> Text:
        return "validate_cust_create_account"

    def validate_name(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict,) -> Dict[Text, Any]:
        if slot_value != None:
            slot_value = NameCorrect(slot_value)
            return {"name": slot_value}
        else:
            return {"name": None}

    def validate_cmnd(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict,) -> Dict[Text, Any]:
        print(len(slot_value))
        if slot_value != None:
            if len(slot_value) == 9 or len(slot_value) == 12:
                print(len(slot_value))
                return {"cmnd": slot_value}
            else:
                dispatcher.utter_message(text=f"S??? cmnd kh??ng h???p l???. Qu?? kh??ch vui l??ng ki???m tra l???i ???.")
                return {"cmnd": None}
        else:
            dispatcher.utter_message(text=f"S??? cmnd kh??ng h???p l???. Qu?? kh??ch vui l??ng ki???m tra l???i ???.")
            return {"cmnd": None}


class ValidateCustSignIn(FormValidationAction):
    def name(self) -> Text:
        return "validate_cust_sign_in"

    def validate_name(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict,) -> Dict[Text, Any]:
        if slot_value != None:
            slot_value = NameCorrect(slot_value)
            return {"name": slot_value}
        else:
            return {"name": None}

    def validate_cmnd(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict,) -> Dict[Text, Any]:
        if slot_value == None:
            dispatcher.utter_message(text=f"S??? cmnd kh??ng h???p l???. Qu?? kh??ch vui l??ng ki???m tra l???i ???.")
            return {"cmnd": None}
        elif len(slot_value) != 12 and len(slot_value) != 9:
            dispatcher.utter_message(text=f"S??? cmnd kh??ng h???p l???. Qu?? kh??ch vui l??ng ki???m tra l???i ???.")
            return {"cmnd": None}
        else:
            return {"cmnd": slot_value}

    def validate_cust_account_number(self,slot_value: Any,dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict,) -> Dict[Text, Any]:
        if slot_value == None or len(slot_value) >= 15 or len(slot_value) < 8:
            dispatcher.utter_message(text=f"s??? t??i kho???n kh??ng h???p l???. Qu?? kh??ch vui l??ng ki???m tra l???i ???.")
            return {"cust_account_number": None}
        else:
            return {"cust_account_number": slot_value}

class ActionResetAccount(Action):

    def name(self):
        return "action_reset_account"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("cust_name", None),
                SlotSet("cust_cmnd", None),
                SlotSet("cust_account_number", None),
                SlotSet("name", None),
                SlotSet("cmnd", None)]

class ActionLogin(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_login"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        count = CheckExist(tracker.get_slot('name').lower(), tracker.get_slot('cmnd'),
                           tracker.get_slot('cust_account_number'))
        if count >= 1:
            cust_name = tracker.get_slot("name")
            cust_name = list(cust_name.split(" "))
            if tracker.get_slot("cust_sex") != "Qu?? kh??ch":
                if cust_name[-1].lower != "anh":
                    return [SlotSet("cust_name", tracker.get_slot('name')),
                            SlotSet("cust_cmnd", tracker.get_slot('cmnd')),
                            SlotSet("login", 'true'),
                            SlotSet("cust_sex", tracker.get_slot("cust_sex") + " " + cust_name[-1])]
                else:
                    return [SlotSet("cust_name", tracker.get_slot('name')),
                            SlotSet("cust_cmnd", tracker.get_slot('cmnd')),
                            SlotSet("login", 'true'),
                            SlotSet("cust_sex", tracker.get_slot("cust_sex") + " " + cust_name[-2:])]
            else:
                return [SlotSet("cust_name", tracker.get_slot('name')),
                        SlotSet("cust_cmnd", tracker.get_slot('cmnd')),
                        SlotSet("login", 'true'),
                        SlotSet("cust_sex", tracker.get_slot("cust_sex"))]
        else:
            return [SlotSet("login", 'false')]

class ActionCreditTransfer(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_transfer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        count = CheckExist(tracker.get_slot('cust_account_number').lower(), tracker.get_slot('receive_transfer_account_number'), tracker.get_slot('credit'))

        acc1 = tracker.get_slot('cust_account_number')
        acc2 = tracker.get_slot('receive_transfer_account_number')
        credit = tracker.get_slot('credit')
        credit = int(credit)
        if (getBalance(acc1) < (credit - 50000)):
            dispatcher.utter_message(text=f"S??? d?? kh??ng ????? ????? th???c hi???n chuy???n kho???n.")
        else:
            newBalance1 = getBalance(acc1) - credit
            newBalance2 = getBalance(acc1) + credit
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE accounts SET balance = {} WHERE account_number = '{}';".format(newBalance1, acc1))
            mycursor.execute("UPDATE accounts SET balance = {} WHERE account_number = '{}';".format(newBalance2, acc2))

            mydb.commit()
            dispatcher.utter_message(text=f"Chuy???n kho???n th??nh c??ng!")

class PromotionalNews(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_feedback_promotion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open('actions/promotional_news.txt', 'r') as f:
            text = f.read()
        dispatcher.utter_message(text=text)

class FeedbackTime(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_feedback_time"
        dispatcher.utter_message(text=text)
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        dispatcher.utter_message(text="B??y gi??? l?? {}".format(current_time))

