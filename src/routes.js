import {
    createBrowserRouter,
} from "react-router-dom";
import SearchView from "./views/SearchView";


export const router = createBrowserRouter([
    {
        path: "/",
        element: <div>Hello world!</div>,
    },
    {
        path: "/search",
        element: <SearchView/>,
    },
]);