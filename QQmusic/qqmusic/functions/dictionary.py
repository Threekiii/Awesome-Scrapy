class CategoryDict():
    def get_language_dict(self):
        language_dict = {
            165: '国语',
            166: '粤语',
            167: '英语',
            168: '韩语',
            169: '日语',
            170: '小语种',
            203: '闽南语',
            204: '法语',
            205: '拉丁语'
        }
        return language_dict


    def get_genre_dict(self):
        genre_dict = {
            6: '流行',
            11: '摇滚',
            15: '轻音乐',
            28: '民谣',
            8: 'R&B',
            153: '嘻哈',
            24: '电子',
            27: '古典',
            18: '乡村',
            22: '蓝调',
            21: '爵士',
            164: '新世纪',
            25: '拉丁',
            218: '后摇',
            219: '中国传统',
            220: '世界音乐'
        }
        return genre_dict


    def get_topic_dict(self):
        topic_dict = {
            39: 'ACG',
            136: '经典',
            146: '网络歌曲',
            133: '影视',
            141: 'KTV热歌',
            131: '儿歌',
            145: '中国风',
            194: '古风',
            148: '情歌',
            196: '城市',
            197: '现场音乐',
            199: '背景音乐',
            200: '佛教音乐',
            201: 'UP主',
            202: '乐器',
            14: 'DJ'
        }
        return topic_dict


    def get_mood_dict(self):
        mood_dict = {
            126: '宣泄',
            68: '思念',
            122: '安静',
            52: '伤感',
            117: '快乐',
            116: '治愈',
            125: '励志',
            59: '甜蜜',
            55: '寂寞'
        }
        return mood_dict


    def get_scene_dict(self):
        scene_dict = {
            78: '睡前',
            102: '夜店',
            101: '学习',
            99: '运动',
            85: '开车',
            76: '约会',
            94: '工作',
            81: '旅行',
            103: '派对',
            222: '婚礼',
            223: '咖啡馆',
            224: '跳舞',
            16: '校园'
        }
        return scene_dict

    def get_all_dict(self):
        all_dict = {}
        all_dict.update(self.get_language_dict())
        all_dict.update(self.get_genre_dict())
        all_dict.update(self.get_topic_dict())
        all_dict.update(self.get_mood_dict())
        all_dict.update(self.get_scene_dict())
        return all_dict

    def number_to_word(self,number):
        all_dict = self.get_all_dict()
        word = all_dict[number]
        return word

    def word_to_number(self,word):
        all_dict = self.get_all_dict()
        number = list(all_dict.keys())[list(all_dict.values()).index(word)]
        return number

class HtmlDict():
    def get_all_dict(self):
        html_char = {}
        html_char['&#10;'] = ''
        html_char['&#13;'] = ' '
        html_char['&#58;'] = ':'
        html_char['&#32;'] = ' '
        html_char['&#38;'] = '&'
        html_char['&#45;'] = '-'
        html_char['&#46;'] = '.'
        html_char['&#40;'] = '('
        html_char['&#41;'] = ')'
        html_char['&#124;'] = '|'
        html_char['&#42;'] = '*'
        html_char['&#39;'] = '\''
        html_char['&#63;'] = '？'
        html_char['&#59;'] = ';'
        html_char['&#33;'] = '!'
        html_char['&#34;'] = '"'
        html_char['&#35;'] = '#'
        html_char['&#37;'] = '%'
        html_char['&#64;'] = '@'
        html_char['&#126;'] = '~'
        html_char['&#9;'] = '   '
        html_char['&#36;'] = '$'
        html_char['&#96;'] = '`'
        html_char['&#95;'] = '_'
        html_char['&#43;'] = '+'
        return html_char

if __name__ == '__main__':
    # print(word_to_number('小语种'))
    dic_func = CategoryDict()
    print(dic_func.number_to_word(int('170')))