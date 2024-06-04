# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HouseItem(scrapy.Item):
    url = scrapy.Field()                        #url
    title = scrapy.Field()                      #标题
    data_frame = scrapy.Field()                 #移动端隐藏数据
    totalArea =  scrapy.Field()                 #根据房屋各个面积求和的总面积
    areaInTitle =  scrapy.Field()               #标题中的总面积
    transactionPrice =  scrapy.Field()          #成交价格
    unitPrice =  scrapy.Field()                 #单价
    source =  scrapy.Field()                    #来源
    transactionTime =  scrapy.Field()           #成交时间
    towards =  scrapy.Field()                   #朝向
    layer = scrapy.Field()                      #楼层
    buildingType =  scrapy.Field()              #楼型
    Elevator =  scrapy.Field()                  #电梯
    decorate =  scrapy.Field()                  #装修
    generation =  scrapy.Field()                #年代
    usage =  scrapy.Field()                     #用途
    ownership =  scrapy.Field()                 #权属
    community =  scrapy.Field()                 #小区
    houseType =  scrapy.Field()                 #房源户型
    InnerArea =  scrapy.Field()                 #套内面积
    houseStructure =  scrapy.Field()            #户型结构
    ratioOfElevatorResidents =  scrapy.Field()  #梯户比例
    equippedWithElevator =  scrapy.Field()      #配备电梯
    transactionOwnership =  scrapy.Field()      #交易权属
    propertyOwnership =  scrapy.Field()         #产权所属
    houseAge =  scrapy.Field()                  #房屋年限
    housingProposes =  scrapy.Field()           #房屋用途
    lianjiaId =  scrapy.Field()                 #链家编号
