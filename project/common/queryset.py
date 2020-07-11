"""


select a.*,b.* FROM a,b;

select count(0) FROM a,b;
select a.*,b.* FROM a,b limit xxx;


select a.xx+b.xx as temp FROM a,b GROUP BY a.id having temp >=1000;
select count(0) FROM a,b GROUP BY a.id
count(SELECT a.*,b.* FROM a,b GROUP BY a.id)


"""

from functools import reduce


from django.db.models.query import QuerySet


class BaseCustomQuerySet(QuerySet):
    """
    拓展查询集里的通用方法，子类通用的链式查询应该放到这里来编写
    """

    def useful(self):
        """ 返回正常可用的数据(未被逻辑删除) """
        return self.filter(deleted=False)

    def useless(self):
        """ 返回已经被删除的数据(逻辑删除) """
        return self.filter(deleted=True)

    def query_id(self, uid, params):
        """ 通用ID查询 """
        return self.useful().filter(uid=uid)
