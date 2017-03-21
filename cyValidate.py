#!/usr/bin/python
# -*- coding: utf-8 -*-

from cySqlite import sqlitedb
from cyEntity import cyEntity

COLUMNS = u' ID,name,spell,content,derivation,samples,first,last '
cy_db = sqlitedb('cy')


def queryById(cy_id):
    sql = u'select %s from CY where ID=%d ' % (COLUMNS, cy_id,)
    cy_rs = cy_db.queryUnique(sql)
    if cy_rs is not None:
        return cyEntity(cy_rs)
    else:
        return None


def queryNameLen(name_len):
    sql = u'select %s from CY where Len(name) = %d' % (COLUMNS, name_len)
    cys = cy_db.query(sql)
    cys_result = []
    if cys is not None and len(cys) > 0:
        for cy_obj in cys:
            cys_result.append(cyEntity(cy_obj))
    return cys_result


def updateName(cy_id, cy_name, cy_spell):
    sql = u'update CY set name="%s",spell="%s" where ID=%d' % (cy_name, cy_spell, cy_id)
    cy_db.dml(sql)


def deletById(cy_id):
    sql = u'delete from CY where ID=%d' % cy_id
    cy_db.dml(sql)


def queryByName(cy_name):
    sql = u'select %s from CY where name=%s' % (COLUMNS, cy_name)
    cys = cy_db.query(sql)
    cys_result = []
    if cys is not None and len(cys) > 0:
        for cy_obj in cys:
            cys_result.append(cyEntity(cy_obj))
    return cys_result


def deleteRepeat():
    names = []
    for i in range(1, 31852):
        cy = queryById(i)
        if cy is not None:
            if cy.name not in names:
                names.append(cy.name)
                print cy.name
            else:
                deletById(cy.id)


def checkSpell():
    temp = [14, 27826, 26024, 26007, 24078, 18984, 15874, 12760, 11020, 9631, 7749, 4709, 4163, 4160,4159, 2490, 3832, 3833, 6229 ]

    # ids = [189, 199, 207, 245, 249, 255, 264, 289, 328, 329, 331, 351, 359, 373, 391, 410, 435, 441, 453, 466, 468, 470, 483, 484, 487, 489, 500, 515, 516, 517, 518, 555, 563, 595, 602, 611, 612, 652, 663, 2490, 3832, 3833, 4159, 4160, 4163, 4709, 4955, 6229, 7749, 8069, 8196, 9631, 11020, 11154, 12760, 14759, 15874, 15960, 18875, 18876, 18984, 21734, 22662, 24078, 25946, 26007, 26021, 26024, 27826, 27843, 30779, 31414, 31657, 31722, 31727, 31769, 31809, 31811, 31820, 31824, 31835, 31836, 31844]

    for i in range(1, 31200):
        cy = queryById(i)
        if cy is not None and cy.id not in temp:
            if len(cy.name.replace("，", " ").replace(" ", "")) != len(cy.spell.replace("，", " ").replace("  ", " ").split(" ")):
                print "|\t %d \t|\t %s \t|\t %s \t\t\t\t|\t %s \t\t|\t %s \t|" % (cy.id, cy.name, cy.first, cy.last, cy.spell)


def queryByNameLen(len):
    cy_nameLen = queryNameLen(len)
    print len(cy_nameLen)
    for cy in cy_nameLen:
        print "|\t %d \t|\t %s \t|\t %s \t\t\t\t|\t %s \t\t|\t %s \t|" % (cy.id, cy.name, cy.first, cy.last, cy.spell)


def queryCount():
    sql = u'select count(1) from CY '
    return cy_db.queryUnique(sql)


ym_map = {}
ym_map['ā'] = 'a'
ym_map['á'] = 'a'
ym_map['ǎ'] = 'a'
ym_map['à'] = 'a'
ym_map['ō'] = 'o'
ym_map['ó'] = 'o'
ym_map['ǒ'] = 'o'
ym_map['ò'] = 'o'
ym_map['ē'] = 'e'
ym_map['é'] = 'e'
ym_map['ě'] = 'e'
ym_map['è'] = 'e'
ym_map['ī'] = 'i'
ym_map['í'] = 'i'
ym_map['ǐ'] = 'i'
ym_map['ì'] = 'i'
ym_map['ū'] = 'u'
ym_map['ú'] = 'u'
ym_map['ǔ'] = 'u'
ym_map["ù"] = "u"
ym_map["ǖ"] = "v"
ym_map["ǘ"] = "v"
ym_map["ǚ"] = "v"
ym_map["ǜ"] = "v"


def getFL(o_str):
    o_arr = [x for x in o_str]
    for key in ym_map.keys():
        for i in range(0, len(o_str)):
            if o_str[i] == key.decode('utf-8'):
                o_arr[i] = ym_map[key]
    return u''.join(o_arr)


def updateFL(f_words, l_words, cy_id):
    sql = u'update CY set first="%s",last="%s" where ID=%d' % (f_words, l_words, cy_id)
    cy_db.dml(sql)


def insert(c_id, c_name, sp, co, vr, sa, fi, la):
    sql = u'insert into CY values (%d,"%s","%s","%s","%s","%s","%s","%s")' % (c_id, c_name, sp, co, vr, sa, fi, la)
    print sql
    cy_db.dml(sql)


def queryByName(c_name):
    sql = u'select %s from CY where name=%s' % (COLUMNS, c_name)
    cy_rs = cy_db.queryUnique(sql)
    if cy_rs is not None:
        return cyEntity(cy_rs)
    else:
        return None


if __name__ == "__main__":
    print queryCount()
    for i in range(1, 30928):
        cy = queryById(i)
        if cy is not None:
            updateFL(getFL(cy.spell.split(' ')[0]), getFL(cy.spell.split(' ')[-1]), cy.id)
            cy = queryById(i)
            print cy.name, cy.first, cy.last
    print 'end'

    cy_db.close()


