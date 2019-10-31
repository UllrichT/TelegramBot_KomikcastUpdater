import json
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def find(id, title):
    # open and read file
    file = open('NewFav.txt','r')
    StringFromFile = file.read()
    file.close()
    # convert JSON_string to dict
    User_fav_list = json.loads(StringFromFile)
    # cek apakah title ada di daftar favorite
    if title in User_fav_list[str(id)]:
        return True
    else:
        return False

def GetUpdate(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai GetUpdate')
    try:
        url = "https://komikcast.com"
        conn = uReq(url)
        getPage = conn.read()
        conn.close()

        getHtml = soup(getPage,"html.parser")
        div = getHtml.findAll('div', {'class' : 'listupd'})
        temp = div[2].findAll('div', {'class': 'luf'})
        for a in range(0,9):
            temp_text = "<a href='ganti1'>ganti2</a>"

            judul = temp[a].find('h3').text
            if find(id, judul):
                judul = '(Fav) ' + judul

            temp2 = temp[a].find('a')
            link = temp2['href']

            temp_text = temp_text.replace('ganti1',link)
            temp_text = temp_text.replace('ganti2', judul)

            chaps = temp[a].findAll('li')
            for b in chaps:
                chap = b.find('a').text
                temp3 = b.find('i').text
                time = '(' + temp3 + ')'
                desc = chap + ' ' + time
                temp_text = temp_text + '\n' + desc
            bot.send_message(chat_id = id, text = temp_text, parse_mode = 'HTML')
    except Exception as e:
        print(e)
    print('\tselesai GetUpdate')

def halo(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai Halo')
    try:
        img_url = 'https://cdn.shopify.com/s/files/1/1960/3689/products/Hello_from_the_otterside_1024x1024@2x.jpg'
        bot.send_photo(chat_id = id, photo = img_url, caption = "Hai\nAda yang bisa saya bantu?\n/GetUpdate\n/ViewFavorite\n/AddFavorite\n/DeleteFavorite")
    except Exception as e:
        print(e)
    print('\tselesai Halo')

def Cancel(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai Cancel')
    try:
        # cek apakah user memiliki request lain yg blm slesai di User_command_list
        if str(id) in User_command_list:
            bot.send_message(chat_id = id, text = "Anda berhenti dari request\n{}".format(User_command_list[str(id)]))
            User_command_list.pop(str(id))
        else:
            bot.send_message(chat_id = id, text = "Anda sedang tidak dalam request apapun")
    except Exception as e:
        print(e)
    print('\tselesai Cancel')

def ViewFavorite(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai ViewFavorite')
    try:
        file = open('NewFav.txt','r')
        StringFromFile = file.read()
        file.close()
        User_fav_list = json.loads(StringFromFile) #convert JSON_string ke dict
        teks = "Berikut adalah daftar favorite anda"
        for a in User_fav_list[str(id)]:
            if a != 'title' :
                teks = teks + '\n\n' + a
        # cek apakah user punya daftar favorite
        if len(User_fav_list[str(id)])>1:
            bot.send_message(chat_id = id, text = teks)
        else:
            bot.send_message(chat_id = id, text = 'Anda tidak memiliki daftar manga favorite')
    except Exception as e:
        print(e)
    print('\tselesai ViewFavorite')

def AddFavorite(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai AddFavorite')
    # cek apakah user sedang berada di tengah request lain
    if str(id) in User_command_list:
        bot.send_message(chat_id = id, text = "Anda sedang di tengah request\n{}".format(User_command_list[str(id)]))
    else:
        bot.send_message(chat_id = id, text = "Silahkan bagikan judul dan link dari manga yg ingin ditambahkan ke daftar favorite\n/Cancel utk membatalkan request")
        User_command_list[str(id)] = "/AddFavorite"
    print('\tselesai AddFavorite')

def DeleteFavorite(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai DeleteFavorite')
    try:
        # cek apakah user sedang berada di tengah request lain
        if str(id) in User_command_list:
            bot.send_message(chat_id = id, text = "Anda sedang di tengah request \n{}".format(User_command_list[str(id)]))
        else:
            file = open('NewFav.txt','r')
            StringFromFile = file.read()
            file.close()
            User_fav_list = json.loads(StringFromFile) #convert JSON_string ke dict
            if str(id) in User_fav_list:
                teks = "Dari daftar judul manga favorite berikut, judul manga manakah yang ingin anda hapus?"
                num = 1
                for a in User_fav_list[str(id)]:
                    if a != 'title':
                        cmd = 'DeleteThisManga{}'.format(str(num))
                        teks = teks + '\n\n' + a + '\n' +'/' + cmd
                        dispatcher.add_handler(CommandHandler(cmd, DeleteHandler))
                        DeleteList.append(a)
                        num += 1
                if len(DeleteList)>0:
                    teks = teks + '\n/Cancel utk membatalkan request'
                    bot.send_message(chat_id = id, text = teks)
                    User_command_list[str(id)] = "/DeleteFavorite"
                else:
                    bot.send_message(chat_id = id, text = 'Anda tidak memiliki daftar manga favorite')
            else:
                bot.send_message(chat_id = id, text = "Anda tidak memiliki daftar manga favorite")
    except Exception as e:
        print(e)
    print('\tselesai DeleteFavorite')

def DeleteHandler(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tstart DeleteHandler')
    try:
        if str(id) in User_command_list:
            if User_command_list[str(id)] == '/DeleteFavorite':
                teks = update.message.text
                temp = teks.split('DeleteThisManga')
                num = int(temp[1])-1
                bot.send_message(chat_id = id, text = teks + '\nApakah anda yakin ingin menghapus \n\n{} \n\ndari daftar favorite?\n/Yes\n/No'.format(DeleteList[num]))
                dispatcher.add_handler(CommandHandler('Yes', DeleteFavoriteNext))
                dispatcher.add_handler(CommandHandler('No', DeleteFavoriteNext))
                User_command_list[str(id)] = '/DeleteFavorite{}'.format(str(num))
            else:
                bot.send_message(chat_id = id, text = 'Anda sedang tidak dalam request \n/DeleteFavorite')
        else:
            bot.send_message(chat_id = id, text = 'Anda sedang tidak dalam request \n/DeleteFavorite')
    except Exception as e:
        print(e)
    print('\tselesai DeleteHandler')

def DeleteFavoriteNext(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tstart DeleteFavoriteNext')
    try:
        teks = update.message.text
        print(TempDel)
        if teks == '/Yes':
            # open and read file
            file = open('NewFav.txt','r')
            StringFromFile = file.read()
            file.close()
            User_fav_list = json.loads(StringFromFile)
            # mengecek di User_command_list, yg mana yg akan didelete
            temp = User_command_list[str(id)]
            temp2 = temp.split('DeleteFavorite')
            num = int(temp2[1])
            User_fav_list[str(id)].pop(DeleteList[num])
            temp_write = json.dumps(User_fav_list)
            # save ke file
            file = open('NewFav.txt','w')
            file.write(temp_write)
            file.close()
            #
            bot.send_message(chat_id = id, text = "Berhasil menghapus \n\n{}\n\n dari daftar favorite".format(DeleteList[num]))
            print('delete \n{}'.format(DeleteList[num]))
        else:
            temp = User_command_list[str(id)]
            temp2 = temp.split('DeleteFavorite')
            num = int(temp2[1])
            bot.send_message(chat_id = id, text = "Batal menghapus \n\n{}\n\ndari daftar favorite".format(DeleteList[num]))
            print('tdk jadi delete \n{}'.format(DeleteList[num]))
        User_command_list.pop(str(id))
    except Exception as e:
        print(e)
    print('\tselesai DeleteFavoriteNext')

def MsgHandler(bot, update):
    id = update.message.chat_id
    print('\nrequest from {}'.format(id))
    print('\tmulai AddFavoriteNext')
    try:
        if str(id) in User_command_list :
            if User_command_list[str(id)] == "/AddFavorite":
                # open and read file
                file = open('NewFav.txt','r')
                StringFromFile = file.read()
                file.close()
                # convert json string ke dict
                if StringFromFile == "":
                    User_fav_list = {"User_id" : "Fav_list"}
                else:
                    User_fav_list = json.loads(StringFromFile)
                # split text message ke title & link
                temp1 = update.message.text
                temp2 = temp1.split('\n')
                temp3 = temp2[0]
                title = temp3.replace(' – Komikcast','')
                link = temp2[1]
                print('title : ' + title)
                print('link  : ' + link)
                # cek apakah chat_id sdh ada di User_fav_list
                if str(id) in User_fav_list:
                    print('user id sdh ada')
                    # kalo sdh ada di daftar favorite
                    if title in User_fav_list[str(id)]:
                        print('Judul manga sdh ada dlm daftar favorite')
                        bot.send_message(chat_id = id, text = "Manga tersebut sdh dlm list favorite")
                    else:
                        print('Judul manga blm ada, menambahkan ke daftar favorite')
                        User_fav_list[str(id)][title] = link
                        bot.send_message(chat_id = id, text = "Berhasil menambahkan \n<b>{}</b> \ndgn link : \n{} \nke daftar favorite".format(title, link), parse_mode = "HTML")
                else:
                    print('user id blm ada')
                    User_fav_list[str(id)] = {"title" : "link"}
                    User_fav_list[str(id)][title] = link
                    bot.send_message(chat_id = id, text = "Berhasil menambahkan \n<b>{}</b> \ndgn link : \n{} \nke daftar favorite".format(title, link), parse_mode = "HTML")
                # save ke file
                temp_write = json.dumps(User_fav_list)
                file = open('NewFav.txt','w')
                file.write(temp_write)
                file.close()
        else:
            bot.send_message(chat_id = id, text = "Mohon maaf, tapi saya tdk mengerti maksud anda")
        User_command_list.pop(str(id))
        print('\tselesai AddFavoriteNext')
    except Exception as e:
        print(e)

# MAIN
print('bot start working')

TOKEN = '936769906:AAEfpuYvytu4D6P5HPGX5Ya0OY_jPTMds8o'
User_command_list = {"User_id" : "command"}
DeleteList = []
TempDel = ""

updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher
bot = telegram.Bot(token = TOKEN)

dispatcher.add_handler(CommandHandler('GetUpdate', GetUpdate))
dispatcher.add_handler(CommandHandler('AddFavorite', AddFavorite))
dispatcher.add_handler(CommandHandler('ViewFavorite', ViewFavorite))
dispatcher.add_handler(CommandHandler('DeleteFavorite', DeleteFavorite))
dispatcher.add_handler(CommandHandler('Cancel', Cancel))
dispatcher.add_handler(CommandHandler('start', halo))
dispatcher.add_handler(MessageHandler(Filters.text, MsgHandler))

updater.start_polling()
updater.idle()
