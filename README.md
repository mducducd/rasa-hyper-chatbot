# rasachatbot

site-packages/rasa/nlu/tokenizers/vi_tokenizer.py

```
import re
from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from underthesea import word_tokenize
class VietnameseTokenizer(Tokenizer):

    provides = [TOKENS_NAMES[attribute] for attribute in MESSAGE_ATTRIBUTES]

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        super().__init__(component_config)

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        words = word_tokenize(text)

        return self._convert_words_to_tokens(words, text)
```
site-packages/rasa/nlu/registry.py
add VietnameseTokenizer into component_classes

mysql structure:
```
    sql = 'create table services(service VARCHAR(255));' \
          'ALTER TABLE service CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;'\
          'INSERT INTO services(service) VALUES("Đăng ký tài khoản");' \
          'INSERT INTO services(service) VALUES("Xem số dư tài khoản");' \
          'INSERT INTO services(service) VALUES("Xem số dư tài khoản");' \
          'INSERT INTO services(service) VALUES("Chuyển khoản");' \
          'CREATE TABLE accounts (full_name VARCHAR(255), id_card VARCHAR(255) , account_number VARCHAR(255),balance INT, PRIMARY KEY(account_number));' \
```
