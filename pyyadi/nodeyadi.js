require('./data.js')
const path = require('path')
const csv  = require('./node_modules/fast-csv/')

rows = [ { 'code':'code', 'name':'name', 'address':'address', 'tel':'tel', 'gps':'gps', 'level':'level', 'openTime':'openTime', 'isClose':'isClose'}]
for (var k1 in storeData) {
    for (var k2 in storeData[k1]) {
        for (var k3 in storeData[k1][k2]) {
            for (var k4 in storeData[k1][k2][k3]) {
                store = storeData[k1][k2][k3][k4]
                rows.push(store)
                console.log(
                    store["code"],
                    store["name"],
                    store["address"],
                    store["tel"],
                    store["gps"],
                    store["level"],
                    store["openTime"],
                    store["isClose"],
                )
            }
        }
    }
}

csv.writeToPath(path.resolve(__dirname, 'yadi.csv'), rows)
    .on('error', err => console.error(err))
    .on('finish', () => console.log('Done writing.'))
