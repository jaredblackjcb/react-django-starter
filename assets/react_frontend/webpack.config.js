const path = require("path");
const webpack = require("webpack");
// const { StatsWriterPlugin } = require("webpack-stats-plugin");

module.exports = {
  entry: "./assets/frontend/src/index.js",
  output: {
    path: path.resolve(__dirname, "./../../static"),
    filename: "js/index-bundle.js",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  resolve: {
    modules: [path.resolve(__dirname, "./../../node_modules")],
    extensions: [".js", ".jsx"],
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("development"),
    }),
    // new StatsWriterPlugin({
    //   filename: "js/webpack-stats.json",
    // }),
  ],
};
