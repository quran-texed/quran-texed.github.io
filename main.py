import yuag
import pyautogui
yuag.clear()

nums = ["١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩", "٠"]

whole_quran: list[str] = yuag.readJSON("./القرآن كتابة/whole_quran_tashkeel.json")
soar_names: list[str] = yuag.readJSON("./القرآن كتابة/soar_names.json")
pages: list[dict] = yuag.readJSON("./القرآن كتابة/pages.json")

def to_arabic_num(num: str):
    num = str(num)

    en = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    for i in range(10):
        num = num.replace(en[i], nums[i])

    return num

def get_sora_index(sura: str):
    return soar_names.index(sura)

def get_soar_indexes(sura_from: str, sura_to: str):
    return list(range(get_sora_index(sura_from), get_sora_index(sura_to)+1))

def get_sura_ayat_count(sura: str|int):
    if type(sura) == str:
        return len(whole_quran[sura])
    elif type(sura) == int:
        return len(whole_quran[soar_names[sura]])

def get_ayat_from_sura(sura: str|int, aya_from: int, aya_to: int):
    if aya_from == aya_to: print(aya_from, sura)
    
    if type(sura) == str:
        return "{ " + " ".join(whole_quran[sura][aya_from-1:aya_to]).replace("﴿", "(").replace("﴾", ")") + " }" + f"\n[سورة {sura}: " + (f"{to_arabic_num(aya_from)}-{to_arabic_num(aya_to)}]" if aya_from != aya_to else f"{to_arabic_num(aya_from)}]")
    elif type(sura) == int:
        return "{ " + " ".join(whole_quran[soar_names[sura]][aya_from-1:aya_to]).replace("﴿", "(").replace("﴾", ")") + " }" + f"\n[سورة {sura}: " + (f"{to_arabic_num(aya_from)}-{to_arabic_num(aya_to)}]" if aya_from != aya_to else f"{to_arabic_num(aya_from)}]")

def get_ayat_from_page(page: int):
    text = ""
    if page % 2 == 0: text = "ا ⬜️⬛️"
    else: text = "ا ⬛️⬜️"

    if pages[page-1]["from_sura"] == pages[page-1]["to_sura"]:
        return text + "\n\n" + get_ayat_from_sura(pages[page-1]["from_sura"], pages[page-1]["from_ayah"], pages[page-1]["to_ayah"]) + "\n\n صفحة " + str(page)
    else:
        res = []
        indexes = get_soar_indexes(pages[page-1]["from_sura"], pages[page-1]["to_sura"])
        for i, ind in enumerate(indexes):
            if i == 0: res.append(get_ayat_from_sura(soar_names[ind], pages[page-1]["from_ayah"], get_sura_ayat_count(soar_names[ind])))
            elif i == len(indexes) - 1: res.append(get_ayat_from_sura(soar_names[ind], 1, pages[page-1]["to_ayah"]))
            else: res.append(get_ayat_from_sura(soar_names[ind], 1, get_sura_ayat_count(soar_names[ind])))
        
        return text + "\n\n" + "\n\n".join(res) + "\n\n صفحة " + str(page)

yuag.wait(5)
for i in range(587, 604+1):
    yuag.copy(get_ayat_from_page(i))
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    yuag.wait(0.5)

yuag.doneMessage(0)

"""
282 البقرة
176 النساء
43 الرعد
45 فاطر
75 الزمر
29 الفتح
22 المجادلة
20 المزمل
25 الانشقاق
3 النصر
"""