class CategoryList():
    def get_language_list(self):
        language_list = ['华语', '欧美', '日语', '韩语', '粤语']
        return language_list

    def get_genre_list(self):
        genre_list = ['流行', '摇滚', '民谣', '电子', '舞曲', '说唱', '轻音乐', '爵士', '乡村', 'R&B/Soul', '古典',
                      '民族', '英伦', '金属', '朋克', '蓝调', '雷鬼', '世界音乐', '拉丁', 'New Age', '古风', '后摇', 'Bossa Nova']
        return genre_list

    def get_scene_list(self):
        scene_list = ['清晨', '夜晚', '学习', '工作', '午休', '下午茶', '地铁', '驾车', '运动', '旅行', '散步', '酒吧']
        return scene_list

    def get_mood_list(self):
        # mood_list = ['怀旧']
        mood_list = ['怀旧', '清新', '浪漫', '伤感', '治愈', '放松', '孤独', '感动', '兴奋', '快乐', '安静', '思念']
        return mood_list

    def get_topic_list(self):
        topic_list = ['影视原声', 'ACG', '儿童', '校园', '游戏', '00后', '70后', '80后', '90后', '网络歌曲', 'KTV', '经典', '翻唱', '吉他',
                      '钢琴', '器乐', '榜单']
        return topic_list

    def get_all_list(self):
        language_list = self.get_language_list()
        genre_list = self.get_genre_list()
        scene_list = self.get_scene_list()
        mood_list = self.get_mood_list()
        topic_list = self.get_topic_list()
        all_list = language_list + genre_list + scene_list + mood_list + topic_list
        return all_list

if __name__ == '__main__':
    offset_list = [n*35 for n in range(0,10)]
    print(offset_list)



