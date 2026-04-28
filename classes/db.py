import os
from dotenv import load_dotenv
import postgrest
from supabase import create_client, Client

class Db:

    def __init__(self):
        load_dotenv()
        self.url = os.environ.get('SUPABASE_URL')
        self.key = os.environ.get('SUPABASE_KEY')

    def getSupabase(self):
        return create_client(self.url, self.key)

    # select query
    def getTableDataQuery(self, table, options):
        response = self.getSupabase().table(table).select(options).execute()

        return response.data
    
    # select with where condition
    def getTableDataQueryWhere(self, table, options, whereKey, whereValue):
        response = self.getSupabase().table(table).select(options).eq(whereKey, whereValue).execute()

        return response.data

    # insert query
    def insert(self, table, query):
        try:
            # get last id on table and add 1 to insert new item - supabase python client has no auto increment id
            result = self.getSupabase().table(table).select("id").order("id", desc=True).limit(1).execute()
            max_id = result.data[0]["id"] if result.data else None
            query["id"] = int(max_id)+1 if max_id is not None else 1
            
            return self.getSupabase().table(table).insert(query).execute()
        except postgrest.exceptions.APIError as error:
            return error.message

    # update query
    def update(self, table, query, conditionKey, conditionValue):
        return self.getSupabase().table(table).update(query).eq(conditionKey, conditionValue).execute()
    
    # delete query
    def delete(self, table, conditionKey, conditionValue):
        self.getSupabase().table(table).delete().eq(conditionKey, conditionValue).execute()
    