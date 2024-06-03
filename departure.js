import {headers} from "./headers.js";
import axios, {getAdapter} from "axios";

async function getAirportDeparture(code , year , month , day , hourOfDay) {
    try {
        const response = await axios.get(`https://api.flightstats.com/flex/flightstatus/rest/v2/json/airport/status/${code}/dep/${year}/${month}/${day}/${hourOfDay}`, headers);
        return response.data;
    } catch (error) {
        console.error('Error making GET request:', error.response ? error.response.data : error.message);
    }
}

async function getDepartures(airport_list , year , month , day , hourOfDay) {
    const arrivalPromises = airport_list.map(airport => getAirportDeparture(airport.fs , year , month , day , hourOfDay));
    return await Promise.all(arrivalPromises);
}

export {getDepartures , getAirportDeparture};