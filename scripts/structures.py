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

    def get_tuple(self, primary_key, page_identify):
        for memored_tuple in self.pages[page_identify].new_tuples:
            if memored_tuple[self.primary_key] == primary_key:
                return memored_tuple

        return None

    def get_num_pages(self):
        return len(self.pages)

    def insert(self, new_tuple) -> bool:

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
        self.num_overflows = 0
        self.num_colisions = 0

        self.buckets = list()
        for i in range(num_buckets):
            # OBS1: buckets[i][0] --> Posições regulares do bucket
            # OBS2: buckets[i][1] --> Posições de overflow do bucket
            self.buckets.append((list(), list()))


    def get_tuple(self, value):
        bucket_index = self.hash_function(value, self.num_buckets)
        num_accessed_pages = 1
        for i in self.buckets[bucket_index][0]:
            if i[0] == value:
                page_index = i[1]
                return self.table_master.get_tuple(value, page_index), page_index, num_accessed_pages 

        for i in self.buckets[bucket_index][1]:
            if i[0] == value:
                page_index = i[1]
                return self.table_master.get_tuple(value, page_index), page_index, num_accessed_pages

        return None, None, None


    def get_tuple_seq_search(self, value):
        
        num_pages = self.table_master.get_num_pages()

        for page_index in range(num_pages):
            memored_tuple = self.table_master.get_tuple(value, page_index)
            if memored_tuple:
                return  memored_tuple, page_index, page_index+1


        return None, None, None


    def get_num_colisions(self):
        return self.num_colisions


    def get_num_overflows(self):
        return self.num_overflows


    def add_tuple(self, tuple) -> bool:
        value = str(tuple[self.table_master.get_primary_key()])
        tuple[self.table_master.get_primary_key()] = value

        bucket_id = self.hash_function(value, self.num_buckets)

        self.table_master.insert(tuple)

        if len(self.buckets[bucket_id][0]) >= self.bucket_size:
            self.num_overflows += 1
            self.buckets[bucket_id][1].append((value, self.table_master.last_page))
        else:
            if len(self.buckets[bucket_id][0]) > 0:
                self.num_colisions += 1
            self.buckets[bucket_id][0].append((value, self.table_master.last_page))



    def hash_function(self, input, normalize_max_value):
        seed = 2654435761
        hash_value = seed
    
        for i, char in enumerate(input):
            hash_value ^= (ord(char) + i) * seed # Comparação XOR
            hash_value = (hash_value << 5) | (hash_value >> 27)  # Rotaciona bits para misturar mais

        # "Normalização"
        hash_value = abs(hash_value) % normalize_max_value

        return hash_value
