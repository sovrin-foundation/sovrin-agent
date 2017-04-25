#!groovy

@Library('SovrinHelpers') _

def name = 'sovrinagent'

def testUbuntu = {
    try {
        echo 'Ubuntu Test: Checkout csm'
        checkout scm

        echo 'Ubuntu Test: Build docker image'
        orientdb.start()

        def testEnv = dockerHelpers.build(name)

        testEnv.inside('--network host') {
            echo 'Ubuntu Test: Install dependencies'
            //testHelpers.install()
            sh "pip install pytest"
            sh "pip install -r requirements.txt"

            echo 'Ubuntu Test: Test'
            testHelpers.testJUnit(resFile: "test-result.${NODE_NAME}.xml")
        }
    }
    finally {
        echo 'Ubuntu Test: Cleanup'
        orientdb.stop()
        step([$class: 'WsCleanup'])
    }
}

def testWindows = {
    echo 'TODO: Implement me'
}

def testWindowsNoDocker = {
    echo 'TODO: Implement me'
}


//testAndPublish(name, [ubuntu: testUbuntu, windows: testWindowsNoDocker, windowsNoDocker: testWindowsNoDocker])
testAndPublish(name, [ubuntu: testUbuntu])
