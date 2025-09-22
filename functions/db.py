import os
from dotenv import load_dotenv
import postgrest
from supabase import create_client, Client

class Db:

    def __init__(self):
        load_dotenv()
        self.url = os.environ.get('SUPABASE_URL')
        self.key = os.environ.get('SUPABASE_KEY')
        self.supabase = create_client(self.url, self.key)

    def getSupabase(self):
        return self.supabase

    # select query
    def getTableDataQuery(self, table, options):
        response = self.supabase.table(table).select(options).execute()

        return response.data
    
    # select with where condition
    def getTableDataQueryWhere(self, table, options, whereKey, whereValue):
        response = self.supabase.table(table).select(options).eq(whereKey, whereValue).execute()

        return response.data

    # insert query
    def insert(self, table, query):
        try:
            return self.supabase.table(table).insert(query).execute()
        except postgrest.exceptions.APIError as error:
            return error.message

    # update query
    def update(self, table, query, conditionKey, conditionValue):
        return self.supabase.table(table).update(query).eq(conditionKey, conditionValue).execute()
    
    # delete query
    def delete(self, table, conditionKey, conditionValue):
        self.supabase.table(table).delete().eq(conditionKey, conditionValue).execute()
    