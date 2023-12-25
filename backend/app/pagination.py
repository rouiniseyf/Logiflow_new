def paginate(records,records_per_page ,page):
    

    records_count = records.count()
    if records_count % records_per_page > 0 : 
        page_count = records_count // records_per_page + 1
    else: 
        page_count = records_count // records_per_page 

    has_next = True 
    has_previous = True  
    next_page = 0 
    previous_page = 0

    if page_count == 1 :
        has_next = False
        has_previous = False 

    else : 
        
        if page == 1 : 
            has_previous = False
        
        elif page == page_count : 
            has_next = False 

    if has_next : 
        next_page = int(page) + 1 
    
    if has_previous :
        previous_page = int(page) - 1

    sliced_records = records[((page-1) * records_per_page):(page * records_per_page)] 


    return [
        sliced_records, 
        {"records_count": records_count,
        "page_count": page_count,
        "has_next": has_next,
        "has_previous": has_previous,
        "next_page": next_page,
        "previous_page": previous_page,
        "page":page,
        "records_per_page" : records_per_page
        }, 
    ]


