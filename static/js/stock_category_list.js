function batch_categories() {
    let stockCategories = $('#stock_categories').children();
    let stockCategoryList = [];
    for (let i = 0; i < stockCategories.length; i++) {
        stockCategoryList.push(
            {
                id: Number.parseInt($(stockCategories[i]).attr('data-id')),
                name: $(stockCategories[i]).attr('data-name')
            }
        )
    }
    return stockCategoryList;
}

let categories = batch_categories();
let type_quantity = [
    {"type": "pc", "name": "шт."},
    {"type": "g", "name": "гр."},
    {"type": "m", "name": "м."},
];