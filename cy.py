#!/usr/bin/python
# -*- coding: utf-8 -*-

from cySqlite import sqlitedb
from cyEntity import cyEntity
import sys

reload(sys)
sys.setdefaultencoding('utf8')


CY_FAIL = U'CY_FAIL'
CY_INPUT_ERROR = u'CY_INPUT_ERROR'
COLUMNS = u' ID,name,spell,content,derivation,samples,first,last '
cy_db = sqlitedb('cy')
HASE_ANWSERED_CY = ['0', ]


def checkIfCY(input_cy):
    sql = u'select %s from CY where name="%s"' % (COLUMNS, input_cy.decode('utf8'))
    check_cy = cy_db.queryUnique(sql)
    return cyEntity(check_cy) if check_cy is not None else None


def queryNext(input_cy):
    check_cy_entity = checkIfCY(input_cy)
    if check_cy_entity is not None:
        HASE_ANWSERED_CY.append(str(check_cy_entity.id))
        result_cy = queryByLast(check_cy_entity.last)
        if result_cy is not None:
            HASE_ANWSERED_CY.append(str(result_cy.id))
            return result_cy
        else:
            return CY_FAIL
    else:
        return CY_INPUT_ERROR


def queryByLast(cy_last):
    used_id = ','.join(HASE_ANWSERED_CY)
    sql = u'select %s from CY where ID not in (%s) and first="%s"' % (COLUMNS, used_id, cy_last)
    result_cy = cy_db.queryUnique(sql)
    return cyEntity(result_cy) if result_cy is not None else None


def checkJLCy(pre_last, next_input):
    check_cy = checkIfCY(next_input)
    if check_cy is None:
        repeat_input = raw_input(u"非成语，请重新输入 -> ")
        return checkJLCy(pre_last, repeat_input)
    elif check_cy is not None and check_cy.first != pre_last:
        repeat_input = raw_input(u"接龙失败，请重新输入 -> ")
        return checkJLCy(pre_last, repeat_input)
    else:
        return next_input


def checkCY(i_cy):
    query_next = queryNext(i_cy)
    if query_next == CY_FAIL:
        return CY_FAIL
    elif query_next == CY_INPUT_ERROR:
        repeat_input = raw_input(u"非成语，请重新输入 -> ")
        return checkCY(repeat_input)
    else:
        print u'电脑回答-> %s | %s' % (query_next.name, query_next.spell)
        next_input = raw_input(u"请输入下一个成语 -> ")
        return checkCY(checkJLCy(query_next.last, next_input))


if __name__ == "__main__":
    i_cy = raw_input(u"请输入第一个成语 -> ")
    print checkCY(i_cy)


