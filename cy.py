#!/usr/bin/python
# -*- coding: utf-8 -*-

from cydb import db
from cyEntity import cyEntity
import spell

COLUMNS = u' ID,name,spell,content,derivation,samples,first,last,spell_new '
cy_db = db('cy')
HASE_ANWSERED_CY = [0, ]


def queryById(cy_id):
    sql = u'select %s from CY where ID=%d' % (COLUMNS, cy_id)
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


if __name__ == "__main__":
    # cy_nameLen = queryNameLen(11)
    # print len(cy_nameLen)
    # for cy in cy_nameLen:
    #     print "|\t %d \t|\t %s \t|\t %s \t\t\t\t|\t %s \t\t|\t %s \t|" % (cy.id, cy.name, cy.first, cy.last, cy.spell)
    for i in range(1, 31852):
        cy = queryById(i)
        if cy is not None:
            if len(cy.name.replace("，", " ").replace(" ", "")) != len(cy.spell.replace("，", " ").replace("  ", " ").split(" ")):
                print "|\t %d \t|\t %s \t|\t %s \t\t\t\t|\t %s \t\t|\t %s \t|" % (cy.id, cy.name, cy.first, cy.last, cy.spell)

    # updateName(59, u'成人不自在，自在不成人', u'chéng rén bù zì zài，zì zài bù chéng rén')
    # updateName(61, u'成则为王，败则为贼', u'chéng zé wéi wáng ，bài zé wéi zéi')
    # updateName(72, u'仇人相见，分外眼红', u'chóu rén xiāng jiàn，fèn wài yǎn hóng')

    print 'end'

    cy_db.close()


