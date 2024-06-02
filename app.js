const express = require('express');
const config = require('./config').port;
const axios = require('axios');

const app = express();


const appID = 'b2c60344';
const appKEY = '791a3fd9091491e167de077578128ec1';

app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile)

const headers = {

    headers: {
        appId: appID,
        appKey: appKEY
    }

}

async function getFilteredAirports() {
    try {
        const response = await axios.get('https://api.flightstats.com/flex/airports/rest/v1/json/active', headers);
        const airports = response.data.airports;

        const filteredAirports = airports.filter(airport => airport.classification === 1);

        return filteredAirports.map(airport => ({
            name: airport.name,
            fs: airport.fs,
            countryName: airport.countryName,
            timeZoneRegionName: airport.timeZoneRegionName,
            localTime: airport.localTime
        }));
    } catch (error) {
        console.error('Error making GET request:', error.response ? error.response.data : error.message);
    }
}


async function getAirportDelays(codes) {
    try {
        const response = await axios.get(`https://api.flightstats.com/flex/delayindex/rest/v1/json/airports/${codes}`, headers);
        return response.data.delayIndexes;


    } catch (error) {
        console.error('Error making GET request:', error.response ? error.response.data : error.message);
    }
}

async function getAirportSchedule(code) {
    try {
        const response = await axios.get(`https://api.flightstats.com/flex/delayindex/rest/v1/json/airports/${code}`, headers);
        return response.data;
    } catch (error) {
        console.error('Error making GET request:', error.response ? error.response.data : error.message);
    }
}

async function getSchedules(airport_list) {
    const schedulePromises = airport_list.map(airport => getAirportSchedule(airport.fs));
    return await Promise.all(schedulePromises);
}



async function getAirlines() {
    try {
        const response = await axios.get(`https://api.flightstats.com/flex/airlines/rest/v1/json/active`, headers);
        console.log(response.data);
        const airlines = response.data.airlines;
        return airlines.map(airline => ({
            name: airline.name,
            fs: airline.fs,
            active: airline.active
        }));


    } catch (error) {
        console.error('Error making GET request:', error.response ? error.response.data : error.message);
    }
}

async function main() {
    const airports_data = await getFilteredAirports();
    const airportCodes = airports_data.map(airport => airport.fs).join(',');


    const airlines = await getAirlines();
    const delay_data = await getAirportDelays(airportCodes);
    //console.log(airlines);
    const schedules = await getSchedules(airports_data);

    console.log(schedules);


}

main();
