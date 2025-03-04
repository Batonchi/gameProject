from database import Connection
from app.texts.model import GetText, CreateText


class TextService:

    @staticmethod
    def save(text: CreateText):
        with Connection() as connection:
            cur = connection.cursor()
            cur.execute('''INSERT INTO texts content VALUES ?''', (text.content,))

    @staticmethod
    def get_text_by_id(text_id: int) -> GetText:
        with Connection() as connection:
            cur = connection.cursor()
            result = cur.execute('''SELECT * FROM texts WHERE text_id = ?''', (text_id,)).fetchone()
            return GetText(result[0], result[1])

d_A1 = {
    'text': '''Эта история – история поучительная, местами занимательная и интересная, история, показывающая, как делать не надо или как нужно реагировать на какие-либо “раздражители”. 
Возможно, кому-то история покажется странной и местами непонятной, но в любом случае, этот рассказ дает понять, что всякое бывает в жизни. Ну что-ж, позвольте, мы начнем повествование.
''',
    'next': {
        'text': '''
Каково человеку находиться в мире иллюзий? В своем собственном мире или ином, выдуманным? Что он чувствует?
''',
        'next': None
    }
}

d1_1 = {
    'text': '''Что за черт? Где я? Почему.. Почему я ничего не помню? Что происходит?''',
    'next': {
        'text': '''Юноша, попрошу вас не выражаться при людях, кто намного старше вас, это некрасиво.
         Ах, да. Вы сейчас находитесь, грубо говоря.. в своем внутреннем мире, но к сожалению,
          полностью непонятном, неоткрытом и неизведанном.''',
        'next': {
            'text': '''Что? Я не понимаю. Мой внутренний мир? Неоткрытый? Это шутка какая-то?''',
            'next': {
                'text': '''Нет. Какие шутки? Вы потеряли себя в поисках “дружбы”, в лицемерии, дабы понравиться обществу.
                 Как вы однажды сказали: “Быть одним из них – это круто”.
                 Туфта. Друг мой, вы потеряли себя и забыли кем являйтесь, и являлись. Но ничего, я помогу вам.''',
                'next': {
                    'text': '''Кто вы?! Что вы от меня хотите?''',
                    'next': {
                        'text': '''Я лишь хочу донести до вас, что вы не замечали очень многое в общении
                         со своими “друзьями”. Ну да ладно. Вам пора идти. Возьмите ключ, он прямо перед вами,
                          подойдите к двери и откройте к ее. ''',
                        'next': {
                            'text': '''Я ничего не буду делать!
                             Либо вы возвращайте меня домой, либо я прямо сейчас вам бошку сверну.''',
                            'next': {
                                'text': '''Какого?''',
                                'next': None
                            }
                        }
                    }
                }
            }
        }
    }
}

d2_1 = {
    'text': '''В бар идем сегодня?''',
    'next': {
        'text': '''– Конечно, договаривались же. Обзвони всех наших только, напомни, что встречаемся в 22:30.''',
        'next': {
            'text': '''Океей, а этому, <nickname>, звонить, он вроде говорил, что хочет с нами пойти.''',
            'next': {
                'text': '''Да на кой он нам нужен. Всю тусу испортит.''',
                'next': {
                    'text': '''Понял)''',
                    'next': None
                }
            }
        }
    }
}

d3_1 = {
    'text': '''Что это было? Почему?.. Что происходит.''',
    'next': None
}

d4_1 = {
    'text': '''Ну, что идем?''',
    'next': {
        'text': '''Подожди пару минут, надо еще ребят дождаться.''',
        'next': {
            'text': '''<nickname>,  если я не ошибаюсь, ты был против этой затеи? Что же ты пришел?''',
            'next': {
                'text': '''Я..''',
                'next': {
                    'text': '''Хватит. Что вы с ним возитесь, пришел и пришел. Вон, там наши подходят, пошли''',
                    'next': None
                }
            }
        }
    }
}

d5_1 = {
    'text': '''Успокоился?''',
    'next': {
        'text': '''Я не понимаю что происходит. Объясните мне.''',
        'next': {
            'text': '''Оставим это на потом. Ты лучше посмотри на эту красоту. ''',
            'next': {
                'text': '''Вы сейчас серьезно?! Я нахожусь не понятно где, вижу своих друзей,
                 которые говорят всякую чушь, а вы мне тут предлагайте на деревце посмотреть?!''',
                'next': {
                    'text': '''Наблюдение за природой способствует лучшему пониманию самого себя,
                     помогает развить терпение, внимательность и умение ценить момент.
                     Советую почаще заниматься этим делом.''',
                    'next': {
                        'text': '''Так я услышу ответ на свой вопрос?''',
                        'next': {
                            'text': '''Да, но не сейчас.
                             Я хочу, чтобы ты посмотрел на себя и своих товарищей со стороны.''',
                            'next': {
                                'text': '''Зачем вы это делайте? Кто вы?''',
                                'next': None
                            }
                        }
                    }
                }
            }
        }
    }
}

d6_1 = {
    'text': '''Как же он надоел. Непонятно что ли, что ему не рады, зачем так навязываться?''',
    'next': {
        'text': '''Видимо нравиться ему так)''',
        'next': None
    }
}

d7_1 = {
    'text': '''Слышал, что <nickname>, перевелся со своего факультета? ''',
    'next': {
        'text': '''Что? Он же был лучшим в потоке? <nickname> реально перевелся к ним? Сумасшедший.''',
        'next': {
            'text': '''Ага, он действительно с ума сошел. Он ведь даже не понимает, что они его используют,
             а нас <nickname> уже не замечает, мол, не достигли нужного уровня развития. Ну смешно же.''',
            'next': {
                'text': '''Дурак, да и только. ''',
                'next': None
            }
        }
    }
}

d8_1 = {
    'text': '''– Наблюдая за тобой, я действительно не понимал, что движет тебя стремиться привлечь к себе внимание
     и добиться признания окружающих. Зачем стремиться быть принятым там, где тебя никогда и не замечали,
      где над тобой всегда смеялись и считали странным? Это бессмысленно, друг мой.
       Когда мы только встретились, я сказал тебе, что ты потерял себя.
        Я докажу тебе это, и, возможно, до тебя дойдет.''',
    'next': {
        'text': '''А что, если меня все устраивает в моей жизни? Я не хочу перемен.
         Со мной стали общаться, разговаривать, я перестал быть тенью.''',
        'next': {
            'text': '''Я докажу, что это не стоило твоих жертв.''',
            'next': {
                'text': '''Жертв? Каких еще жертв? По-моему я никого не убивал)''',
                'next': {
                    'text': '''Шутки шутишь – это отлично. Открывай дверь и иди дальше.''',
                    'next': None
                }
            }
        }
    }
}

d_A2 = {
    'text': '''Человек может навязывать своё общение, чтобы знать и слышать,
     что он чего-то стоит, что он для кого-то важен и интересен.
      Навязанные желания прочно закрепляются в подсознании человека и воспринимаются как собственные, отражающие личные
       потребности, из-за чего, человек может и не заметить, как отказывается от того,
        что ему было действительно дорого и ценно.''',
    'next': None
}

d1_2 = {
    'text': '''Любимый плеер. Раньше он был всегда со мной и во включенном состоянии.
     На него закачены все треки “Call Me Karizma”, один из самых любимых исполнителей. Был.''',
    'next': None
}

d2_2 = {
    'text': '''Как много книг. По-моему все прочитаны. Удивительно, что нет ни одного комикса''',
    'next': None
}

d3_2 = {
    'text': '''Словари. Так и не добил я испанский.''',
    'next': None
}

d4_2 = {
    'text': '''Как много книг. По-моему все прочитаны. Удивительно, что нет ни одного комикса.''',
    'next': None
}

d5_2 = {
    'text': '''А этого здесь не было. Это.. ключ?''',
    'next': None
}

d6_2 = {
    'text': '''Плеер все тот же.''',
    'next': None
}

d7_2 = {
    'text': '''Книги.. Их меньше. Куда я их дел?''',
    'next': None
}

d8_2 = {
    'text': '''а столе бардак. Словари валяются, все в исписанных листочках. Почерк кстати красивый)''',
    'next': None
}

d9_2 = {
    'text': '''Еще один ключ?''',
    'next': None
}

d10_2 = {
    'text': '''Плеер потрепало знатно, не работает.''',
    'next': None
}

d11_2 = {
    'text': '''От книг и не осталось и следа. Одна белиберда с комиксами осталась,
     как я мог вообще это читать и убрать нормальные книги, куда я классику дел?''',
    'next': None
}

d12_2 = {
    'text': '''На рабочем столе ничего нет, удивительное явление.
     В детстве у меня всегда творился хаус в виде различных листочков с сочинениями или рисунками.''',
    'next': None
}

d13_2 = {
    'text': '''Ну конечно, еще один ключ.''',
    'next': None
}

d14_2 = {
    'text': '''Можно вечно смотреть на огонь.. Тем более тогда, когда что-то горит, не так ли, друг мой?''',
    'next': {
        'text': '''О чем вы?''',
        'next': {
            'text': '''Как тебе комнаты?''',
            'next': {
                'text': '''Да ничего, мои же. Правда содержимое с годами поменялось, я бы сказал знатно.
                 В последней почти ничего не осталось из первой.''',
                'next': {
                    'text': '''Можно бесконечно смотреть на то, как горит огонь, тем более, когда в нем что-то горит,
                     например, какие-нибудь листочки с глупым содержанием, или..''',
                    'next': {
                        'text': '''На что вы намекайте?''',
                        'next': {
                            'text': '''А ты забыл, что сам избавился от того, что тебе всегда нравилось?''',
                            'next': {
                                'text': '''Я.. я не понимаю. Я просто познакомился с новыми ребятами, пригласил
                                 их к себе домой. Зайдя ко мне в комнату они всего лишь..''',
                                'next': {
                                    'text': '''Сказали: “Что за скукота и как ты здесь живешь?” - не так ли?''',
                                    'next': {
                                        'text': '''Да, но я же не.. Они знают лучше меня..''',
                                        'next': {
                                            'text': '''Что тебе нравиться?''',
                                            'next': {
                                                'text': '''Почему вы меня перебивайте?! Стойте! НЕТ!''',
                                                'next': None
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

d15_2 = {
    'text': '''Я просто хотел понравиться им, чтобы они приняли меня в свою компанию.. Я не знал, что выйдет все так.''',
    'next': None
}

d_A3 = {
    'text': '''Как легко заставить человека сомневаться. Нужно всего лишь надавить на слабые места и воуля.  
    На сколько тяжело принять человеку тот факт, что он тратил свои время, силы, возможности зря?
     И каков будет его выбор: продолжать жить также или быть собой и забить на всех?
''',
    'next': None
}

d1_3 = {
    'text': '''Ты навязывался ко всем, не замечая, как начинаешь всем надоедать.''',
    'next': None
}

d2_3 = {
    'text': '''Начал забываться, отказываться от своих интересов, от того, что всегда нравилось. Ради чего?''',
    'next': None
}

d3_3 = {
    'text': '''Ты считал, что быть одним из них – это самое лучшее, что может произойти с тобой.
     В какой момент ты начал жить этим: подражание этим соплякам стало чуть ли не смыслом твоей жизни,
      ты стал притворяться и врать самому себе. ''',
    'next': None
}

d4_3 = {
    'text': '''Врал и не понимал, что начинаешь терять себя. ''',
    'next': None
}

d5_3 = {
    'text': '''Стоило оно того? Кто-нибудь может стал интересоваться тобой?
     Может кто-нибудь хоть раз тебя выслушал и послушал? ''',
    'next': None
}

d6_3 = {
    'text': '''Так что? Стоило оно того?''',
    'next': {
        'text': '''Кто вы?''',
        'next': {
            'text': '''Я тот, кто останется в твоей памяти на очень долгое время, друг мой.
             Ну, а сейчас, я покидаю и оставляю тебя в глубоких размышлениях. Просыпайся.''',
            'next': {
                'text': '''Что? ''',
                'next': None
            }
        }
    }
}

d_A4 = {
    'text': '''The end.''',
    'next': None
}