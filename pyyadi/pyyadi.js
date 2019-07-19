const request = require('request');
const fs = require("fs");
const path = require('path')
const csv  = require('./node_modules/fast-csv/')


request('https://www.yadea.com.cn/scripts/storeData.js', function (error, response, body) {
    console.log('statusCode:', response && response.statusCode);
    js_obj = body.split("window._")[1].slice(0, -15)
    //console.log(js_obj.slice(0,100))
    //console.log(js_obj.slice(-100))

    fs.writeFile("./data.js", js_obj, (err) => {
        console.log("Successfully Written to data.js");
        require('./data.js')
        rows = [ { 'code':'code', 'name':'name', 'address':'address', 'tel':'tel', 'gps':'gps', 'level':'level', 'openTime':'openTime', 'isClose':'isClose'}]
        for (var k1 in storeData) {
            for (var k2 in storeData[k1]) {
                for (var k3 in storeData[k1][k2]) {
                    for (var k4 in storeData[k1][k2][k3]) {
                        store = storeData[k1][k2][k3][k4]
                        rows.push(store)
                    }
                }
            }
        }

        csv.writeToPath(path.resolve(__dirname, 'yadi.csv'), rows)
            .on('error', err => console.error(err))
            .on('finish', () => console.log('Done writing CSV.'))

    }); //end of write file
}); //end of request


