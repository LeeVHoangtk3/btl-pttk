package com.qltc.util;

import java.sql.*;
public class DatabaseConnection {
private DatabaseConnection() { }
    /** Mo ket noi rieng cho tung thao tac; caller phai dong ket noi. */
    public static Connection open() throws SQLException {
        String url = System.getenv("QLTC_DB_URL");
        if (url == null) url = "jdbc:mysql://localhost:3306/qltc_db";
        return DriverManager.getConnection(url,
            System.getenv("QLTC_DB_USER"), System.getenv("QLTC_DB_PASSWORD"));
    }
}
