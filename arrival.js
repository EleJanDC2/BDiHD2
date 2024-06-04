import {headers} from "./headers.js";
import axios from "axios";

async function getAirportArrival(code , year , month , day , hourOfDay) {
    try {
        const response = await axios.get(`https://api.flightstats.com/flex/flightstatus/rest/v2/json/airport/status/${code}/arr/${year}/${month}/${day}/${hourOfDay}`, headers);
        return response.data;
    } catch (error) {
        console.error('Error making GET request:', error.response ? error.response.data : error.message);
    }
}





export {getAirportArrival};