import {headers} from "./headers.js";
import axios from "axios";


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

async function getFilteredByCountryAirports(countryCode) {
    try {

        const response = await axios.get('https://api.flightstats.com/flex/airports/rest/v1/json/active', headers);
        const airports = response.data.airports;

        let filteredAirports = airports.filter(airport => airport.classification >= 2);
        filteredAirports = filteredAirports.filter(airport => airport.countryCode === countryCode);



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

export {getFilteredAirports , getFilteredByCountryAirports}