/**
 * Order the rows of a table according to a specific column.
 */
const sortTable = ({ tbody, column, reverse, attributes, dates }) => {
    const selector = `td:eq(${column})`;

    // The data to order can be gotten from either the cell text itself or from the 'order-data-1' and 'order-data-2' attributes, since ordering by the text is not always suitable. For example names might want to be ordered by surname but written as "<first_names> <surname>".
    let getFirstData, getSecondData;
    if (attributes) {
        getFirstData = a => $(selector, a).attr("order-data-1") || "";
        getSecondData = a => $(selector, a).attr("order-data-2") || "";
    } else {
        getFirstData = a =>  $(selector, a).text();
        getSecondData = () => "";
    }

    let rows = tbody.find("tr");
    let compareFn;
    if (dates) {
        compareFn = (a, b) => {
            const a1 = new Date(getFirstData(a));
            const b1 = new Date(getFirstData(b));
            if (b1 > a1) return 1;
            if (a1 > b1) return -1;

            const a2 = new Date(getSecondData(a));
            const b2 = new Date(getSecondData(b));
            if (b2 > a2) return 1;
            if (a2 > b2) return -1;
            return 0;
        }
    } else {
        // localeCompare() can also compare numbers as strings when the 'numeric' option is set
        const options = { usage: "sort", sensitivity: "base", numeric: true };

        // XXX: The locale is hardcoded to 'sv' here, but it should probably be handled in some other way
        compareFn = (a, b) => {
            const result = getFirstData(b).localeCompare(getFirstData(a), "sv", options);
            if (result !== 0) return result;
            return getSecondData(b).localeCompare(getSecondData(a), "sv", options);
        }
    }

    if (reverse) {
        rows = rows.sort((a, b) => compareFn(a, b));
    } else {
        rows = rows.sort((a, b) => compareFn(b, a));
    }
    rows.appendTo(tbody);
}


$(document).ready(() => {
    /**
     * Setup tables to be sortable by listening for clicks on '.order-by' columns. The order is reversed if the same column is clicked twice in a row. The data location and method of comparison can be changed by adding the classes 'attributes' and 'dates'.
     */
    $(".order-by").each((_, e) => {
        const tbody = $(e).closest("thead").next("tbody");
        if (!tbody) return;

        const column = $(e).closest("th").index().toString();

        e.onclick = () => {
            const by = tbody.attr("order-by");
            let reverse = Boolean(tbody.attr("order-reverse"));
            if (by === column) reverse = !reverse;
            sortTable({
                tbody,
                column,
                reverse,
                attributes: $(e).hasClass("attributes"),
                dates: $(e).hasClass("dates"),
            });
            tbody.attr("order-by", column);
            tbody.attr("order-reverse", reverse ? "1" : "");
        }
    });
});
