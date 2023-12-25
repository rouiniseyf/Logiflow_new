import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider  } from "react-router-dom";
import Login from "./routes/Login";
import Root from "./routes/Root";
import PrestationsGroupage from "./routes/PrestationsGroupage";
import PrestationsConteneur from "./routes/PrestationsConteneur";
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import Gros from "./routes/gros/index";

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      { path: "/prestations/groupage", element:  <PrestationsGroupage /> },
      { path: "/prestations/conteneur", element:  <PrestationsConteneur /> },
      { path: "/gros", element:  <Gros /> },
    ],
  },
  {
    path: "/login",
    element: <Login />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
    <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
);
