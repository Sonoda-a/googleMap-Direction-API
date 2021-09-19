import urllib.request, json
import urllib.parse
import datetime
import csv
import sys
from tkinter import filedialog


#Google Maps Platform Directions API endpoint
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = ''

#CSVファイルの読み込み
file_name = filedialog.askopenfilename(
    title = 'CSVファイルを開く',
    filetypes = [('csv file', '.csv')],
    initialdir = './' # 自分自身のディレクトリ
    )
if not file_name:
    print('csvファイルを選択していないので終了しました。')
    sys.exit()

# システム時間の取得とcsv出力ファイル名の作成
dt_now = datetime.datetime.now()
dep_time = dt_now.strftime('%Y/%m/%d %H:%M')
csv_name = dt_now.strftime('%Y%m%d%H%M%S') + '.csv'

# CSVを読み込んで行ごとに出発地／目的地の住所を取り出して計測させる。
csv_file = open(file_name, 'r', encoding='utf-8', errors='', newline='')
f = csv.reader(csv_file, delimiter=',', doublequote=True, lineterminator='\n', quotechar='"', skipinitialspace=True)

result = []
#APIを用いて出発地から目的地までの距離を取得して配列に格納する。
for row in f:
    origin = ''
    destination = ''
    unix_time = 0

    #出発地
    origin = row[0].replace(' ', '+')
    #目的地
    destination = row[1].replace(' ', '+')

    #UNIX時間の算出
    dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
    unix_time = int(dtime.timestamp())

    nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}'.format(origin, destination, unix_time, api_key)
    nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
    request = endpoint + nav_request

    # Google Maps Platform Directions APIを実行
    response = urllib.request.urlopen(request).read()

    # 結果(JSON)を取得
    directions = json.loads(response)

    # 所要時間を取得
    for key in directions['routes']:
        # print(key) # titleのみ参照
        # print(key['legs'])
        distance_text = ''
        distance_value = ''
        duration_in_traffic_text = ''
        duration_in_traffic_value = ''

        for key2 in key['legs']:
            distance_text = key2['distance']['text']
            distance_value = key2['distance']['value']
            duration_in_traffic_text = key2['duration_in_traffic']['text']
            duration_in_traffic_value = key2['duration_in_traffic']['value']

    #結果を格納
    result.append([origin, destination, distance_text, distance_value, duration_in_traffic_text, duration_in_traffic_value])
csv_file.close()

#csvの書き出し
w = open(csv_name, 'w', newline='')
writer = csv.writer(w)
writer.writerows(result)
w.close()

