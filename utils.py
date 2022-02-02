import requests
import json

BASE_URL = "https://kolayik.com/api/v2/"
LIST_URL = "person/list"
VIEW_URL = "person/view/"

# async def get_people_meyer(header, results, people_list):
#     async with aiohttp.ClientSession() as session:
#         tasks = get_people_tasks(session, header, results)
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             temp = await response.json()
#             person = {
#                 'SicilNo': None,
#                 'Ad': temp['data']['person']['firstName'],
#                 'Soyad': temp['data']['person']["lastName"],
#                 'İşe İlk Giriş Tarihi': temp['data']['person']['employmentStartDate'],
#                 'İşten Çıkış Tarihi': None,
#                 'Doğum Tarihi': temp['data']['person']['birthday'],
#                 'TC Kimlik No': temp['data']['person']['idNumber'],
#                 'Email': temp['data']['person']['workEmail'],
#                 'Firma': None,
#                 'Alt Firma': None,
#                 'Bolum': None,
#                 'Pozisyon': None,
#                 'Gorev': None,
#                 'Yaka': None,
#                 'Üst Organizasyon': None,
#                 'Kart No Bilgisi(varsa)': None,
#                 'Yönetici Sicil No': None,
#                 'Yönetici Ad Soyad': None,
#                 'Yonetici Mail Adresi': None,
#                 'Okod1': None,
#                 'Okod2': None,
#                 'Okod3': None,
#                 'Okod4': None
#             }
#             if temp['data']['person']['dataList'] != None:
#                 for y in temp['data']['person']['dataList']:
#                     if y['fieldToken'] == "meyerSicilNo":
#                         person['SicilNo'] = y['value']
#                     if y['fieldToken'] == "kartNoBilgisi":
#                         person['Kart No Bilgisi(varsa)'] = y['value']
#                     if y['fieldToken'] == "yoneticiSicilNo":
#                         person['Yönetici Sicil No'] = y['value']
#                     if y['fieldToken'] == "yoneticiAdSoyad":
#                         person['Yönetici Ad Soyad'] = y['value']
#                     if y['fieldToken'] == "yoneticiMailAdresi":
#                         person['Yonetici Mail Adresi'] = y['value']
#
#             if temp['data']['person']['unitList'] != None:
#                 for i in temp['data']['person']['unitList'][0]['items']:
#                     if i['unitName'] == "Şirket":
#                         person['Firma'] = i['unitItemName']
#                     if i['unitName'] == "Unvan":
#                         person['Gorev'] = i['unitItemName']
#                     if i['unitName'] == "Departman":
#                         person['Bolum'] = i['unitItemName']
#                     if i['unitName'] == "Şube":
#                         person['Alt Firma'] = i['unitItemName']
#             print(person)
#             people_list.append(person)
#
# async def get_people_wipelot(header, results, people_list):
#     async with aiohttp.ClientSession() as session:
#         tasks = get_people_tasks(session, header, results)
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             temp = await response.json()
#             person = {
#                 'SicilNo': temp['data']['person']['id'],
#                 'Ad': temp['data']['person']['firstName'],
#                 'Soyad': temp['data']['person']["lastName"],
#                 'İşe İlk Giriş Tarihi': temp['data']['person']['employmentStartDate'],
#                 'İşten Çıkış Tarihi': None,
#                 'Doğum Tarihi': temp['data']['person']['birthday'],
#                 'TC Kimlik No': temp['data']['person']['idNumber'],
#                 'Email': temp['data']['person']['workEmail'],
#                 'Firma': None,
#                 'Alt Firma': None,
#                 'Bolum': None,
#                 'Pozisyon': None,
#                 'Gorev': None,
#                 'Yaka': None,
#                 'Üst Organizasyon': None,
#                 'Kart No Bilgisi(varsa)': None,
#                 'Yönetici Sicil No': None,
#                 'Yönetici Ad Soyad': None,
#                 'Yonetici Mail Adresi': None,
#                 'Okod1': None,
#                 'Okod2': None,
#                 'Okod3': None,
#                 'Okod4': None
#             }
#             if temp['data']['person']['dataList'] != None:
#                 for y in temp['data']['person']['dataList']:
#                     if y['fieldToken'] == "meyerSicilNo":
#                         person['SicilNo'] = y['value']
#                     if y['fieldToken'] == "kartNoBilgisi":
#                         person['Kart No Bilgisi(varsa)'] = y['value']
#                     if y['fieldToken'] == "yoneticiSicilNo":
#                         person['Yönetici Sicil No'] = y['value']
#                     if y['fieldToken'] == "yoneticiAdSoyad":
#                         person['Yönetici Ad Soyad'] = y['value']
#                     if y['fieldToken'] == "yoneticiMailAdresi":
#                         person['Yonetici Mail Adresi'] = y['value']
#
#             if temp['data']['person']['unitList'] != None:
#                 person['Yönetici Sicil No'] = temp['data']['person']['unitList'][0]['managerId']
#                 for i in temp['data']['person']['unitList'][0]['items']:
#                     if i['unitName'] == "Şirket":
#                         person['Firma'] = i['unitItemName']
#                     if i['unitName'] == "Unvan":
#                         person['Gorev'] = i['unitItemName']
#                     if i['unitName'] == "Departman":
#                         person['Bolum'] = i['unitItemName']
#                     if i['unitName'] == "Birim":
#                         person['Bolum'] = i['unitItemName']
#             print(person)
#             people_list.append(person)

def make_request(method, url, payload, HEADER):
    response = requests.request(method, url, headers=HEADER, data=payload)
    return json.loads(response.text)

def block_function(item, person_list, header):
    people = make_request("GET", BASE_URL + VIEW_URL + item['id'], {}, header)
    print(people)
    person = {
        'SicilNo': item['id'],
        'Ad': item['firstName'],
        'Soyad': item['lastName'],
        'İşe İlk Giriş Tarihi': people['data']['person']['employmentStartDate'],
        'İşten Çıkış Tarihi': None,
        'Doğum Tarihi': people['data']['person']['birthday'],
        'TC Kimlik No': people['data']['person']['idNumber'],
        'Email': people['data']['person']['workEmail'],
        'Firma': people['data']['person']['unitList'][0]['items'][0]['unitItemName'],
        'Alt Firma': None,
        'Bolum': None,
        'Pozisyon': None,
        'Gorev': None,
        'Yaka': None,
        'Üst Organizasyon': None,
        'Kart No Bilgisi(varsa)': None,
        'Yönetici Sicil No': None,
        'Yönetici Ad Soyad': None,
        'Yonetici Mail Adresi': None,
        'Okod1': None,
        'Okod2': None,
        'Okod3': None,
        'Okod4': None
    }
    person_list.append(person)
    return person_list

