#!/usr/bin/python
# -*- coding: utf-8 -*-

from cydb import db
from cyEntity import cyEntity
import spell

COLUMNS = u' ID,name,spell,content,derivation,samples,first,last,spell_new '
cy_db = db('cy')
HASE_ANWSERED_CY = [0, ]


def queryById(cy_id):
    sql = u'select %s from CY where ID=%d ' % (COLUMNS, cy_id,)
    cy_rs = cy_db.queryUnique(sql)
    if cy_rs is not None:
        return cyEntity(cy_rs)
    else:
        return None


def update(cy_id, cy_spell):
    sql = u'update CY set spell_new="%s" where ID=%d' % (cy_spell, cy_id)
    cy_db.dml(sql)


def queryNameLen(name_len):
    sql = u'select %s from CY where Len(name) = %d' % (COLUMNS, name_len)
    cys = cy_db.query(sql)
    cys_result = []
    if cys is not None and len(cys) > 0:
        for cy_obj in cys:
            cys_result.append(cyEntity(cy_obj))
    return cys_result


def queryNext(input_cy):
    sql = u'select %s from CY where name=%s' % (COLUMNS, input_cy)
    check_cy = cy_db.query(sql)
    check_cy_entity = cyEntity(check_cy) if check_cy is not None else None
    if check_cy_entity is not None:
        HASE_ANWSERED_CY.append(check_cy_entity.id)
        result_cy = queryByLast(check_cy_entity.last)
        if result_cy is not None:
            HASE_ANWSERED_CY.append(result_cy.id)
            return result_cy.name
        else:
            return u"接龙失败~~"
    else:
        return u"输入不是成语"


def queryByLast(cy_last):
    used_id = HASE_ANWSERED_CY.join(",")
    sql = u'select %s from CY where ID not in (%s) and first=%s' % (COLUMNS, used_id, cy_last)
    result_cy = cy_db.queryUnique(sql)
    return cyEntity(result_cy) if result_cy is not None else None


def updateName(cy_id, cy_name, cy_spell):
    sql = u'update CY set name="%s",spell="%s" where ID=%d' % (cy_name, cy_spell, cy_id)
    cy_db.dml(sql)

temp = [14]

if __name__ == "__main__":
    # cy_nameLen = queryNameLen(11)
    # print len(cy_nameLen)
    # for cy in cy_nameLen:
    #     print "|\t %d \t|\t %s \t|\t %s \t\t\t\t|\t %s \t\t|\t %s \t|" % (cy.id, cy.name, cy.first, cy.last, cy.spell)

    updateName(31657, u'福兮祸所伏，祸兮福所倚', u'fú xī huò suǒ fú， huò xī fú suǒ yǐ')

    ids = [189, 199, 207, 245, 249, 255, 264, 289, 328, 329, 331, 351, 359, 373, 391, 410, 435, 441, 453, 466, 468, 470, 483, 484, 487, 489, 500, 515, 516, 517, 518, 555, 563, 595, 602, 611, 612, 652, 663, 2490, 3832, 3833, 4159, 4160, 4163, 4709, 4955, 6229, 7749, 8069, 8196, 9631, 11020, 11154, 12760, 14759, 15874, 15960, 18875, 18876, 18984, 21734, 22662, 24078, 25946, 26007, 26021, 26024, 27826, 27843, 30779, 31414, 31657, 31722, 31727, 31769, 31809, 31811, 31820, 31824, 31835, 31836, 31844]

    for i in ids:
        cy = queryById(i)
        if cy is not None and cy.id not in temp:
            if len(cy.name.replace("，", " ").replace(" ", "")) != len(cy.spell.replace("，", " ").replace("  ", " ").split(" ")):
                print "|\t %d \t|\t %s \t|\t %s \t\t\t\t|\t %s \t\t|\t %s \t|" % (cy.id, cy.name, cy.first, cy.last, cy.spell)
            else:
                ids.remove(cy.id)

    print 'end'
    print len(ids)

    cy_db.close()


