緣起
==========
在學運結束後. 有人在 Facebook 上成立了小蜜蜂戰鬥隊

https://www.facebook.com/groups/739964776043615/

這個 project 希望能夠幫助小蜜蜂戰鬥隊
能夠有個容易回報和在地圖上呈現的方式

http://beemap.tw

更多關於這個 project 的資訊. 請參考:

https://g0v.hackpad.com/KOsFaCMi6u0

Project Structure
==========
這個 Project 目前分成以下的 sub-project

LittleBeeGeo-frontend
---------
小蜜蜂回報的 frontend. 
使用 [Angular-Brunch-Seed-Livescript](https://github.com/clkao/angular-brunch-seed-livescript) + [UI.Map](http://angular-ui.github.io/ui-map/) + [ng-grid](http://angular-ui.github.io/ng-grid/)

LittleBeeGeo_backend
---------
小蜜蜂回報的 backend.
使用 [python](https://www.python.org/) + [Bottle](http://www.bottlepy.org)

LittleBeeGeo_crawlers
---------
小蜜蜂回報對於 google spreadsheet 的 crawler.
目前是 spreadsheet 的 parser.
使用 [python](https://www.python.org/)

LittleBeeGeo-crawlers-frontend
---------
小蜜蜂回報的 crawler 的輔助修改 frontend.
使用 [Angular-Brunch-Seed-Livescript](https://github.com/clkao/angular-brunch-seed-livescript)