# Braces Node-Webkit
    Braces is a minimal code editor built with node-webkit.

## Downloading and using node-webkit
    Download the appropriate node-webkit binary from the [node-webkit](https://github.com/rogerwang/node-webkit#wiki-downloads) repo in github. The binary zip comes with a node-webkit command-lie tool which is used to run the app.

## Creating the application
    Write your application as you would write a node.js application and you can even use whatever node-modules you want. The app config goes into the package.json. node-webkit provides a lot of modules to access the native functions, it is as easy as requiring the correct module and using it as you would do for a node.js app.

## Running the application
    Package the folder using zip and you can run the app using

```
$ /path/to/node-webkit zipfile
```