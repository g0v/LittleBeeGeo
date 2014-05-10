'use strict'

{sort-by, map, max, min, head} = require 'prelude-ls'

# 1. use queryGeoInfo to query from google map
# 2. use getGeoInfo to get data from cached_data

_LANDMARK_TYPE_LIST = <[ accounting airport amusement_park aquarium art_gallery atm bakery bank bar beauty_salon bicycle_store book_store bowling_alley bus_station cafe campground car_dealer car_rental car_repair car_wash casino cemetery church city_hall clothing_store convenience_store courthouse dentist department_store doctor electrician electronics_store embassy establishment finance fire_station florist food funeral_home furniture_store gas_station general_contractor grocery_or_supermarket gym hair_care hardware_store health hindu_temple home_goods_store hospital insurance_agency jewelry_store laundry lawyer library liquor_store local_government_office locksmith lodging meal_delivery meal_takeaway mosque movie_rental movie_theater moving_company museum night_club painter park parking pet_store pharmacy physiotherapist place_of_worship plumber police post_office real_estate_agency restaurant roofing_contractor rv_park school shoe_store shopping_mall spa stadium storage store subway_station synagogue taxi_stand train_station travel_agency university veterinary_care zoo ]>

cached_data = 
  data: {}

_COUNTY_BY_POSTAL_CODE_MAP = 
  "100": \台北市
  "103": \台北市
  "104": \台北市
  "105": \台北市
  "106": \台北市
  "108": \台北市
  "110": \台北市
  "111": \台北市
  "112": \台北市
  "114": \台北市
  "115": \台北市
  "116": \台北市
  "200": \基隆市
  "201": \基隆市
  "202": \基隆市
  "203": \基隆市
  "204": \基隆市
  "205": \基隆市
  "206": \基隆市
  "209": \連江縣
  "210": \連江縣
  "211": \連江縣
  "212": \連江縣
  "207": \新北市
  "208": \新北市
  "220": \新北市
  "221": \新北市
  "222": \新北市
  "223": \新北市
  "224": \新北市
  "226": \新北市
  "227": \新北市
  "228": \新北市
  "231": \新北市
  "232": \新北市
  "233": \新北市
  "234": \新北市
  "235": \新北市
  "236": \新北市
  "237": \新北市
  "238": \新北市
  "239": \新北市
  "241": \新北市
  "242": \新北市
  "243": \新北市
  "244": \新北市
  "247": \新北市
  "248": \新北市
  "249": \新北市
  "251": \新北市
  "252": \新北市
  "253": \新北市
  "260": \宜蘭縣
  "261": \宜蘭縣
  "262": \宜蘭縣
  "263": \宜蘭縣
  "264": \宜蘭縣
  "265": \宜蘭縣
  "266": \宜蘭縣
  "267": \宜蘭縣
  "268": \宜蘭縣
  "269": \宜蘭縣
  "270": \宜蘭縣
  "272": \宜蘭縣
  "290": \宜蘭縣
  "300": \新竹市
  "302": \新竹縣
  "303": \新竹縣
  "304": \新竹縣
  "305": \新竹縣
  "306": \新竹縣
  "307": \新竹縣
  "308": \新竹縣
  "310": \新竹縣
  "311": \新竹縣
  "312": \新竹縣
  "313": \新竹縣
  "314": \新竹縣
  "315": \新竹縣
  "320": \桃園縣
  "321": \桃園縣
  "323": \桃園縣
  "324": \桃園縣
  "325": \桃園縣
  "326": \桃園縣
  "327": \桃園縣
  "328": \桃園縣
  "329": \桃園縣
  "330": \桃園縣
  "331": \桃園縣
  "332": \桃園縣
  "333": \桃園縣
  "334": \桃園縣
  "335": \桃園縣
  "336": \桃園縣
  "337": \桃園縣
  "338": \桃園縣
  "350": \苗栗縣
  "351": \苗栗縣
  "352": \苗栗縣
  "353": \苗栗縣
  "354": \苗栗縣
  "356": \苗栗縣
  "357": \苗栗縣
  "358": \苗栗縣
  "360": \苗栗縣
  "361": \苗栗縣
  "362": \苗栗縣
  "363": \苗栗縣
  "364": \苗栗縣
  "365": \苗栗縣
  "366": \苗栗縣
  "367": \苗栗縣
  "368": \苗栗縣
  "369": \苗栗縣
  "400": \台中市
  "401": \台中市
  "402": \台中市
  "403": \台中市
  "404": \台中市
  "406": \台中市
  "407": \台中市
  "408": \台中市
  "411": \台中市
  "412": \台中市
  "413": \台中市
  "414": \台中市
  "420": \台中市
  "421": \台中市
  "422": \台中市
  "423": \台中市
  "424": \台中市
  "426": \台中市
  "427": \台中市
  "428": \台中市
  "429": \台中市
  "432": \台中市
  "433": \台中市
  "434": \台中市
  "435": \台中市
  "436": \台中市
  "437": \台中市
  "438": \台中市
  "439": \台中市
  "500": \彰化縣
  "502": \彰化縣
  "503": \彰化縣
  "504": \彰化縣
  "505": \彰化縣
  "506": \彰化縣
  "507": \彰化縣
  "508": \彰化縣
  "509": \彰化縣
  "510": \彰化縣
  "511": \彰化縣
  "512": \彰化縣
  "513": \彰化縣
  "514": \彰化縣
  "515": \彰化縣
  "516": \彰化縣
  "520": \彰化縣
  "521": \彰化縣
  "522": \彰化縣
  "523": \彰化縣
  "524": \彰化縣
  "525": \彰化縣
  "526": \彰化縣
  "527": \彰化縣
  "528": \彰化縣
  "530": \彰化縣
  "540": \南投縣
  "541": \南投縣
  "542": \南投縣
  "544": \南投縣
  "545": \南投縣
  "546": \南投縣
  "551": \南投縣
  "552": \南投縣
  "553": \南投縣
  "555": \南投縣
  "556": \南投縣
  "557": \南投縣
  "558": \南投縣
  "600": \嘉義市
  "602": \嘉義縣
  "603": \嘉義縣
  "604": \嘉義縣
  "605": \嘉義縣
  "606": \嘉義縣
  "607": \嘉義縣
  "608": \嘉義縣
  "611": \嘉義縣
  "612": \嘉義縣
  "613": \嘉義縣
  "614": \嘉義縣
  "615": \嘉義縣
  "616": \嘉義縣
  "621": \嘉義縣
  "622": \嘉義縣
  "623": \嘉義縣
  "624": \嘉義縣
  "625": \嘉義縣
  "630": \雲林縣
  "631": \雲林縣
  "632": \雲林縣
  "633": \雲林縣
  "634": \雲林縣
  "635": \雲林縣
  "636": \雲林縣
  "637": \雲林縣
  "638": \雲林縣
  "640": \雲林縣
  "643": \雲林縣
  "646": \雲林縣
  "647": \雲林縣
  "648": \雲林縣
  "649": \雲林縣
  "651": \雲林縣
  "652": \雲林縣
  "653": \雲林縣
  "654": \雲林縣
  "655": \雲林縣
  "700": \台南市
  "701": \台南市
  "702": \台南市
  "704": \台南市
  "708": \台南市
  "709": \台南市
  "710": \台南市
  "711": \台南市
  "712": \台南市
  "713": \台南市
  "714": \台南市
  "715": \台南市
  "716": \台南市
  "717": \台南市
  "718": \台南市
  "719": \台南市
  "720": \台南市
  "721": \台南市
  "722": \台南市
  "723": \台南市
  "724": \台南市
  "725": \台南市
  "726": \台南市
  "727": \台南市
  "730": \台南市
  "731": \台南市
  "732": \台南市
  "733": \台南市
  "734": \台南市
  "735": \台南市
  "736": \台南市
  "737": \台南市
  "741": \台南市
  "742": \台南市
  "743": \台南市
  "744": \台南市
  "745": \台南市
  "800": \高雄市
  "801": \高雄市
  "802": \高雄市
  "803": \高雄市
  "804": \高雄市
  "805": \高雄市
  "806": \高雄市
  "807": \高雄市
  "811": \高雄市
  "812": \高雄市
  "813": \高雄市
  "814": \高雄市
  "815": \高雄市
  "817": \高雄市
  "819": \高雄市
  "820": \高雄市
  "821": \高雄市
  "822": \高雄市
  "823": \高雄市
  "824": \高雄市
  "825": \高雄市
  "826": \高雄市
  "827": \高雄市
  "828": \高雄市
  "829": \高雄市
  "830": \高雄市
  "831": \高雄市
  "832": \高雄市
  "833": \高雄市
  "840": \高雄市
  "842": \高雄市
  "843": \高雄市
  "844": \高雄市
  "845": \高雄市
  "846": \高雄市
  "847": \高雄市
  "848": \高雄市
  "849": \高雄市
  "851": \高雄市
  "852": \高雄市
  "880": \澎湖縣
  "881": \澎湖縣
  "882": \澎湖縣
  "883": \澎湖縣
  "884": \澎湖縣
  "885": \澎湖縣
  "890": \金門縣
  "891": \金門縣
  "892": \金門縣
  "893": \金門縣
  "894": \金門縣
  "896": \金門縣
  "900": \屏東縣
  "901": \屏東縣
  "902": \屏東縣
  "903": \屏東縣
  "904": \屏東縣
  "905": \屏東縣
  "906": \屏東縣
  "907": \屏東縣
  "908": \屏東縣
  "909": \屏東縣
  "911": \屏東縣
  "912": \屏東縣
  "913": \屏東縣
  "920": \屏東縣
  "921": \屏東縣
  "922": \屏東縣
  "923": \屏東縣
  "924": \屏東縣
  "925": \屏東縣
  "926": \屏東縣
  "927": \屏東縣
  "928": \屏東縣
  "929": \屏東縣
  "931": \屏東縣
  "932": \屏東縣
  "940": \屏東縣
  "941": \屏東縣
  "942": \屏東縣
  "943": \屏東縣
  "944": \屏東縣
  "945": \屏東縣
  "946": \屏東縣
  "947": \屏東縣
  "950": \台東縣
  "951": \台東縣
  "952": \台東縣
  "953": \台東縣
  "954": \台東縣
  "955": \台東縣
  "956": \台東縣
  "957": \台東縣
  "958": \台東縣
  "959": \台東縣
  "961": \台東縣
  "962": \台東縣
  "963": \台東縣
  "964": \台東縣
  "965": \台東縣
  "966": \台東縣
  "970": \花蓮縣
  "971": \花蓮縣
  "972": \花蓮縣
  "973": \花蓮縣
  "974": \花蓮縣
  "975": \花蓮縣
  "976": \花蓮縣
  "977": \花蓮縣
  "978": \花蓮縣
  "979": \花蓮縣
  "981": \花蓮縣
  "982": \花蓮縣
  "983": \花蓮縣

_TOWN_BY_POSTAL_CODE_MAP = 
  "100": \中正區
  "103": \大同區
  "104": \中山區
  "105": \松山區
  "106": \大安區
  "108": \萬華區
  "110": \信義區
  "111": \士林區
  "112": \北投區
  "114": \內湖區
  "115": \南港區
  "116": \文山區
  "200": \仁愛區
  "201": \信義區
  "202": \中正區
  "203": \中山區
  "204": \安樂區
  "205": \暖暖區
  "206": \七堵區
  "209": \南竿鄉
  "210": \北竿鄉
  "211": \莒光鄉
  "212": \東引鄉
  "207": \萬里區
  "208": \金山區
  "220": \板橋區
  "221": \汐止區
  "222": \深坑區
  "223": \石碇區
  "224": \瑞芳區
  "226": \平溪區
  "227": \雙溪區
  "228": \貢寮區
  "231": \新店區
  "232": \坪林區
  "233": \烏來區
  "234": \永和區
  "235": \中和區
  "236": \土城區
  "237": \三峽區
  "238": \樹林區
  "239": \鶯歌區
  "241": \三重區
  "242": \新莊區
  "243": \泰山區
  "244": \林口區
  "247": \蘆洲區
  "248": \五股區
  "249": \八里區
  "251": \淡水區
  "252": \三芝區
  "253": \石門區
  "260": \宜蘭市
  "261": \頭城鎮
  "262": \礁溪鄉
  "263": \壯圍鄉
  "264": \員山鄉
  "265": \羅東鎮
  "266": \三星鄉
  "267": \大同鄉
  "268": \五結鄉
  "269": \冬山鄉
  "270": \蘇澳鎮
  "272": \南澳鄉
  "290": \釣魚台
#  "300": \新竹市
  "302": \竹北市
  "303": \湖口鄉
  "304": \新豐鄉
  "305": \新埔鎮
  "306": \關西鎮
  "307": \芎林鄉
  "308": \寶山鄉
  "310": \竹東鎮
  "311": \五峰鄉
  "312": \橫山鄉
  "313": \尖石鄉
  "314": \北埔鄉
  "315": \峨眉鄉
  "320": \中壢市
  "324": \平鎮市
  "325": \龍潭鄉
  "326": \楊梅市
  "327": \新屋鄉
  "328": \觀音鄉
  "330": \桃園市
  "333": \龜山鄉
  "334": \八德市
  "335": \大溪鎮
  "336": \復興鄉
  "337": \大園鄉
  "338": \蘆竹鄉
  "350": \竹南鎮
  "351": \頭份鎮
  "352": \三灣鄉
  "353": \南庄鄉
  "354": \獅壇鄉
  "356": \後龍鎮
  "357": \通霄鎮
  "358": \苑裡鎮
  "360": \苗栗市
  "361": \造橋鄉
  "362": \頭屋鄉
  "363": \公館鄉
  "364": \大湖鄉
  "365": \泰安鄉
  "366": \銅鑼鄉
  "367": \三義鄉
  "368": \西湖鄉
  "369": \卓蘭鄉
  "400": \中區
  "401": \東區
  "402": \南區
  "403": \西區
  "404": \北區
  "406": \北屯區
  "407": \西屯區
  "408": \南屯區
  "411": \太平區
  "412": \大里區
  "413": \霧峰區
  "414": \烏日區
  "420": \豐原區
  "421": \后里區
  "422": \石岡區
  "423": \東勢區
  "424": \和平區
  "426": \新社區
  "427": \潭子區
  "428": \大雅區
  "429": \神岡區
  "432": \大肚區
  "433": \沙鹿區
  "434": \龍井區
  "435": \梧棲區
  "436": \清水區
  "437": \大甲區
  "438": \外埔區
  "439": \大安區
  "500": \彰化市
  "502": \芬園鄉
  "503": \花壇鄉
  "504": \秀水鄉
  "505": \鹿港鄉
  "506": \福興鄉
  "507": \線西鄉
  "508": \和美鎮
  "509": \伸港鄉
  "510": \員林鎮
  "511": \社頭鄉
  "512": \永靖鄉
  "513": \埔心鄉
  "514": \溪湖鄉
  "515": \大村鄉
  "516": \埔鹽鄉
  "520": \田中鎮
  "521": \北斗鎮
  "522": \田尾鄉
  "523": \埤頭鄉
  "524": \溪州鄉
  "525": \竹塘鄉
  "526": \二林鎮
  "527": \大城鄉
  "528": \芳苑鄉
  "530": \二水鄉
  "540": \南投市
  "541": \中寮鄉
  "542": \草屯鎮
  "544": \國姓鄉
  "545": \埔里鎮
  "546": \仁愛鄉
  "551": \名間鄉
  "552": \集集鎮
  "553": \水里鄉
  "555": \魚池鄉
  "556": \信義鄉
  "557": \竹山鎮
  "558": \鹿谷鄉
#  "600": \嘉義市
  "602": \番路鄉
  "603": \梅山鄉
#  "604": \嘉義縣
#  "605": \嘉義縣
#  "606": \嘉義縣
#  "607": \嘉義縣
#  "608": \嘉義縣
#  "611": \嘉義縣
#  "612": \嘉義縣
#  "613": \嘉義縣
#  "614": \嘉義縣
#  "615": \嘉義縣
#  "616": \嘉義縣
#  "621": \嘉義縣
#  "622": \嘉義縣
#  "623": \嘉義縣
#  "624": \嘉義縣
#  "625": \嘉義縣
#  "630": \雲林縣
#  "631": \雲林縣
#  "632": \雲林縣
#  "633": \雲林縣
#  "634": \雲林縣
#  "635": \雲林縣
#  "636": \雲林縣
#  "637": \雲林縣
#  "638": \雲林縣
#  "640": \雲林縣
#  "643": \雲林縣
#  "646": \雲林縣
#  "647": \雲林縣
#  "648": \雲林縣
#  "649": \雲林縣
#  "651": \雲林縣
#  "652": \雲林縣
#  "653": \雲林縣
#  "654": \雲林縣
#  "655": \雲林縣
#  "700": \台南市
#  "701": \台南市
#  "702": \台南市
#  "704": \台南市
#  "708": \台南市
#  "709": \台南市
#  "710": \台南市
#  "711": \台南市
#  "712": \台南市
#  "713": \台南市
#  "714": \台南市
#  "715": \台南市
#  "716": \台南市
#  "717": \台南市
#  "718": \台南市
#  "719": \台南市
#  "720": \台南市
#  "721": \台南市
#  "722": \台南市
#  "723": \台南市
#  "724": \台南市
#  "725": \台南市
#  "726": \台南市
#  "727": \台南市
#  "730": \台南市
#  "731": \台南市
#  "732": \台南市
#  "733": \台南市
#  "734": \台南市
#  "735": \台南市
#  "736": \台南市
#  "737": \台南市
#  "741": \台南市
#  "742": \台南市
#  "743": \台南市
#  "744": \台南市
#  "745": \台南市
#  "800": \高雄市
#  "801": \高雄市
#  "802": \高雄市
#  "803": \高雄市
#  "804": \高雄市
#  "805": \高雄市
#  "806": \高雄市
#  "807": \高雄市
#  "811": \高雄市
#  "812": \高雄市
#  "813": \高雄市
#  "814": \高雄市
#  "815": \高雄市
#  "817": \高雄市
#  "819": \高雄市
#  "820": \高雄市
#  "821": \高雄市
#  "822": \高雄市
#  "823": \高雄市
#  "824": \高雄市
#  "825": \高雄市
#  "826": \高雄市
#  "827": \高雄市
#  "828": \高雄市
#  "829": \高雄市
#  "830": \高雄市
#  "831": \高雄市
#  "832": \高雄市
#  "833": \高雄市
#  "840": \高雄市
#  "842": \高雄市
#  "843": \高雄市
#  "844": \高雄市
#  "845": \高雄市
#  "846": \高雄市
#  "847": \高雄市
#  "848": \高雄市
#  "849": \高雄市
#  "851": \高雄市
#  "852": \高雄市
#  "880": \澎湖縣
#  "881": \澎湖縣
#  "882": \澎湖縣
#  "883": \澎湖縣
#  "884": \澎湖縣
#  "885": \澎湖縣
#  "890": \金門縣
#  "891": \金門縣
#  "892": \金門縣
#  "893": \金門縣
#  "894": \金門縣
#  "896": \金門縣
#  "900": \屏東縣
#  "901": \屏東縣
#  "902": \屏東縣
#  "903": \屏東縣
#  "904": \屏東縣
#  "905": \屏東縣
#  "906": \屏東縣
#  "907": \屏東縣
#  "908": \屏東縣
#  "909": \屏東縣
#  "911": \屏東縣
#  "912": \屏東縣
#  "913": \屏東縣
#  "920": \屏東縣
#  "921": \屏東縣
#  "922": \屏東縣
#  "923": \屏東縣
#  "924": \屏東縣
#  "925": \屏東縣
#  "926": \屏東縣
#  "927": \屏東縣
#  "928": \屏東縣
#  "929": \屏東縣
#  "931": \屏東縣
#  "932": \屏東縣
#  "940": \屏東縣
#  "941": \屏東縣
#  "942": \屏東縣
#  "943": \屏東縣
#  "944": \屏東縣
#  "945": \屏東縣
#  "946": \屏東縣
#  "947": \屏東縣
#  "950": \台東縣
#  "951": \台東縣
#  "952": \台東縣
#  "953": \台東縣
#  "954": \台東縣
#  "955": \台東縣
#  "956": \台東縣
#  "957": \台東縣
#  "958": \台東縣
#  "959": \台東縣
#  "961": \台東縣
#  "962": \台東縣
#  "963": \台東縣
#  "964": \台東縣
#  "965": \台東縣
#  "966": \台東縣
#  "970": \花蓮縣
#  "971": \花蓮縣
#  "972": \花蓮縣
#  "973": \花蓮縣
#  "974": \花蓮縣
#  "975": \花蓮縣
#  "976": \花蓮縣
#  "977": \花蓮縣
#  "978": \花蓮縣
#  "979": \花蓮縣
#  "981": \花蓮縣
#  "982": \花蓮縣
#  "983": \花蓮縣

_PRIORITY_MAP = 
  street_number: 0
  premise: 0
  route: 0
  subway_station: 1
  bus_station: 1
  transit_station: 1
  establishment: 1
  sublocality: 2
  locality: 3
  postal_code: 4
  administrative_area_level_2: 5
  country: 6

angular.module 'LittleBeeGeoFrontend'
  .factory 'geoData', <[ $http constants ]> ++ ($http, constants)->
    # Service logic
    # ...

    _query_success = (data, status, headers, config) ->
      console.log '_query_success: data:', data, 'status:', status, 'headers:', headers!, 'config:', config
      latlon = config.params.latlng
      if latlon in cached_data.data
        return

      _update_data data, status, headers, config

    _update_data = (data, status, headers, config) ->
      data_status = data.status
      if data_status != "OK"
        console.log 'geoData._update_data: status is not OK: data', data
        return

      latlon = config.params.latlng

      {county, town, address, street_number, landmark} = _parse_data data

      console.log 'setup data: latlon:', latlon, 'county:', county, 'town:', town, 'address:', address, 'street_number:', street_number, 'landmark:', landmark

      cached_data.data[latlon] = {county, town, address, street_number, landmark}

    _parse_priority = ->
      the_types = it.types

      console.log 'the_types', the_types

      max_priority = 0
      for each_type in the_types
        console.log 'each_type:', each_type
        each_priority = _PRIORITY_MAP[each_type]
        if each_priority is void
          continue
        console.log 'each_prioirty:', each_priority, 'each_type:', each_type
        max_priority = max max_priority, each_priority

      it['priority'] = max_priority


    _parse_data = (data) ->
      results = data.results
      if results is void
        return ''

      results |> map _parse_priority

      results |> sort-by (.priority)

      postal_code = ''
      county = ''
      town = ''
      address = ''
      landmark = ''
      
      for each_result in results
        if postal_code and country and town and address and establishment
          break

        address_components = each_result.address_components

        # postal code for county and town
        if not postal_code
          for each_address_component in address_components
            the_types = each_address_component.types
            for each_type in the_types
              if each_type == 'postal_code'
                postal_code = each_address_component.short_name
                break
            if postal_code
              break

          if postal_code
            county = _COUNTY_BY_POSTAL_CODE_MAP[postal_code]
            town = _TOWN_BY_POSTAL_CODE_MAP[postal_code]

        # county
        if not county
          for each_address_component in address_components
            the_types = each_address_component.types
            for each_type in the_types
              if each_type == 'administrative_area_level_2'
                county = each_address_component.long_name
                break
            if county
              break

        # town
        if not town
          for each_address_component in address_components
            the_types = each_address_component.types
            for each_type in the_types
              if each_type == 'locality'
                town = each_address_component.long_name
                break
            if town
              break

        # address
        if not address
          for each_address_component in address_components
            the_types = each_address_component.types
            for each_type in the_types
              if each_type == 'route'
                address = each_address_component.long_name
                break
            if address
              break

        if not address
          for each_address_component in address_components
            the_types = each_address_component.types
            for each_type in the_types
              if each_type in _LANDMARK_TYPE_LIST
                address = each_address_component.long_name
                break
            if address
              break

        # street number
        for each_address_component in address_components
          the_types = each_address_component.types
          for each_type in the_types
            if each_type == 'street_number'
              street_number = parseInt each_address_component.long_name.replace /號$/, ''
              break
          if address
            break

        #landmark
        if not landmark
          for each_address_component in address_components
            the_types = each_address_component.types
            for each_type in the_types
              if each_type in _LANDMARK_TYPE_LIST
                landmark = each_address_component.long_name
                break
            if landmark
              break

      console.log 'postal_code:', postal_code, 'county:', county, 'town:', town, 'address:' address, 'street_number:', street_number, 'landmark:', landmark

      {county, town, address, street_number, landmark}

    _query_error = (data, status, headers, config) ->
      latlon = config.latlng
      if latlon in cached_data.data
        return

      console.log 'geoData._query_error: latlon:', latlon

    _query_geo_info = (latlon) ->
      url = 'https://maps.googleapis.com/maps/api/geocode/json'

      params =
        language: \zh-tw
        sensor: false
        latlng: latlon

      console.log 'to http_get: url:', url, 'params:', params

      $http {method: \GET, url, params}
        .success _query_success
        .error _query_error

    # Public API here
    do 
      queryGeoInfo: (latlng) ->
        lat = latlng.lat!
        lon = latlng.lng!

        latlon = (lat.toFixed 4) + ',' + (lon.toFixed 4)

        console.log 'lat:', lat, 'lon:', 'latlon:', latlon

        if latlon in cached_data.data
          return

        _query_geo_info latlon

      getGeoInfo: (latlng) ->
        console.log 'latlng:', latlng
        lat = latlng.lat!
        lon = latlng.lng!

        latlon = (lat.toFixed 4) + ',' + (lon.toFixed 4)

        console.log 'latlon:', latlon, 'cached_data.data:', cached_data.data

        result = cached_data.data[latlon]
          
        if result is void
          console.log 'latlon not in cached_data.data'
          return {county: '', town: '', address: ''}

        result
