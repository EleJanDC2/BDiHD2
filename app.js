import express from 'express';
import serverPort from "./config.js";
import axios from "axios";
import {headers} from './headers.js';
import {getArrivals , getAirportArrival} from "./arrival.js";
import {getDepartures , getAirportDeparture} from "./departure.js";
import {getFilteredAirports, getFilteredByCountryAirports} from "./filterAirports.js";
import ejs from 'ejs'

const app = express();



app.set('view engine', 'html');
app.engine('html', ejs.renderFile)



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
    const airports_GB = await getFilteredByCountryAirports("GB");

    console.log(airports_GB);

    const airlines = await getAirlines();
    const delay_data = await getAirportDelays(airportCodes);
    //console.log(airlines);
    const schedules = await getSchedules(airports_data);

    //console.log(schedules);

    const year = 2024
    const month = 6
    const day = 2
    const hour = 16

    const arrivals = await  getArrivals(airports_data , year , month , day , hour);
    const arrival = await getAirportArrival(airports_data[0].fs , year , month , day , hour);
    console.log(arrival);

    const departures = await  getDepartures(airports_data , year , month , day , hour);
    const departure = await getAirportDeparture(airports_data[0].fs , year , month , day , hour);
    console.log(departure);


}

main();
