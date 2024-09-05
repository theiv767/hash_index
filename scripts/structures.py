# ESTRUTURAS DE DADOS: TUPLA, PÁGINA, TABELA, BUCKET



class new_tuple:
    def __init__(self, fields) -> None:
        self.fields = fields

    def get_field_value(self, field_name):
        return self.fields[field_name]

    def set_field_value(self, field_name, new_field_value) -> None:
        self.fields[field_name] = new_field_value

#-------------------------------------------------------------------

class Page:
    def __init__(self, identify) -> None:
        self.id = identify
        self.new_tuples = list()
        pass

    def add_new_tuple(self, new_tuple):
        self.new_tuples.append(new_tuple)
        pass

    def get_page_Lenght(self):
        return len(self.new_tuples)

#-------------------------------------------------------------------

class Table:
    def __init__(self, fields, primary_key, page_size=300) -> None:
        self.last_page = 0
        self.primary_key = primary_key
        self.field_names = fields
        self.pages = list()
        self.pages.append( Page(self.last_page) )
        self.page_size = page_size


    def get_primary_key(self):
        return self.primary_key

    def get_record(self, primary_key, page_identify):
        for memored_tuple in self.pages[page_identify].new_tuples:
            if memored_tuple[self.primary_key] == primary_key:
                return memored_tuple

        return None


    def insert(self, new_tuple) -> bool:
        #todo --> verificar se a primary_key está preenchida

        new_tuple_field_names = list(new_tuple.keys())

        for field in self.field_names:
            if not (field in new_tuple_field_names):
                new_tuple[field] = None
                new_tuple_field_names.append(field)

            if len(new_tuple_field_names) > len(self.field_names):
                return False

        if new_tuple[self.primary_key] == None:
            return False


        if self.pages[self.last_page].get_page_Lenght() >= self.page_size:
            new_page = Page(self.last_page+1)
            self.last_page += 1
            self.pages.append(new_page)


        self.pages[self.last_page].add_new_tuple(new_tuple)


        return True


    def delete(self) -> bool:
        pass

#-------------------------------------------------------------------

class Bucket:
    def __init__(self, num_buckets, bucket_size, table_master) -> None:
        self.table_master = table_master
        self.num_buckets = num_buckets
        self.bucket_size = bucket_size

        self.buckets = list()
        for i in range(num_buckets):
            self.buckets.append(list())

    def get_record(self, value):
        bucket_index = self.hash_function(value, self.num_buckets)
        for i in self.buckets[bucket_index]:
            if i[0] == value:
                page_index = i[1]
                return self.table_master.get_record(value, page_index)

        return None



    def add_value(self, tuple) -> bool:
        value = tuple[self.table_master.get_primary_key()]

        bucket_id = self.hash_function(value, self.num_buckets)

        self.table_master.insert(tuple)

        self.buckets[bucket_id].append((value, self.table_master.last_page))



    def hash_function(self, input, normalize_max_value):
        ascii_sum = sum(ord(char) ** 3 for char in input)

        # normalização
        hash_value = ascii_sum % normalize_max_value

        return hash_value