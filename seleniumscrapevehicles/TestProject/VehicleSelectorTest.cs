using SeleniumTestMain.General;

using System;
using OpenQA.Selenium;
using NUnit.Framework;

namespace TestProject
{
    
    
    /// <summary>
    ///This is a test class for VehicleSelectorTest and is intended
    ///to contain all VehicleSelectorTest Unit Tests
    ///</summary>
    [TestFixture]
    public class VehicleSelectorTest {


        private TestContext testContextInstance;

        /// <summary>
        ///Gets or sets the test context which provides
        ///information about and functionality for the current test run.
        ///</summary>
        public TestContext TestContext {
            get {
                return testContextInstance;
            }
            set {
                testContextInstance = value;
            }
        }

        #region Additional test attributes
        // 
        //You can use the following additional attributes as you write your tests:
        //
        //Use ClassInitialize to run code before running the first test in the class
        //[ClassInitialize()]
        //public static void MyClassInitialize(TestContext testContext)
        //{
        //}
        //
        //Use ClassCleanup to run code after all tests in a class have run
        //[ClassCleanup()]
        //public static void MyClassCleanup()
        //{
        //}
        //
        //Use TestInitialize to run code before running each test
        //[TestInitialize()]
        //public void MyTestInitialize()
        //{
        //}
        //
        //Use TestCleanup to run code after each test has run
        //[TestCleanup()]
        //public void MyTestCleanup()
        //{
        //}
        //
        #endregion


        /// <summary>
        ///A test for SelectMake
        ///</summary>
        [Test]
        public void SelectMakeTest() {
            IWebDriver driver = null; // TODO: Initialize to an appropriate value
            VehicleSelector target = new VehicleSelector(driver); // TODO: Initialize to an appropriate value
            target.SelectMake();
            Assert.Inconclusive("A method that does not return a value cannot be verified.");
        }

        /// <summary>
        ///A test for DragSlider
        ///</summary>
        [Test]
        public void DragSliderTest() {
            IWebDriver driver = null; // TODO: Initialize to an appropriate value
            VehicleSelector target = new VehicleSelector(driver); // TODO: Initialize to an appropriate value
            target.DragSlider();
            Assert.Inconclusive("A method that does not return a value cannot be verified.");
        }

        /// <summary>
        ///A test for SelectModel
        ///</summary>
        [Test]
        public void SelectModelTest() {
            IWebDriver driver = null; // TODO: Initialize to an appropriate value
            VehicleSelector target = new VehicleSelector(driver); // TODO: Initialize to an appropriate value
            target.SelectModel();
            Assert.Inconclusive("A method that does not return a value cannot be verified.");
        }

        /// <summary>
        ///A test for CheckModelIsPresent
        ///</summary>
        [Test]
       
        public void CheckModelIsPresentTest() {
            PrivateObject param0 = null; // TODO: Initialize to an appropriate value
            VehicleSelector_Accessor target = new VehicleSelector_Accessor(param0); // TODO: Initialize to an appropriate value
            string model = string.Empty; // TODO: Initialize to an appropriate value
            bool expected = false; // TODO: Initialize to an appropriate value
            bool actual;
            actual = target.CheckModelIsPresent(model);
            Assert.AreEqual(expected, actual);
            Assert.Inconclusive("Verify the correctness of this test method.");
        }

        /// <summary>
        ///A test for CheckMakeIsPresent
        ///</summary>
        [Test]
       
        public void CheckMakeIsPresentTest() {
            PrivateObject param0 = null; // TODO: Initialize to an appropriate value
            VehicleSelector_Accessor target = new VehicleSelector_Accessor(param0); // TODO: Initialize to an appropriate value
            string make = string.Empty; // TODO: Initialize to an appropriate value
            bool expected = false; // TODO: Initialize to an appropriate value
            bool actual;
            actual = target.CheckMakeIsPresent(make);
            Assert.AreEqual(expected, actual);
            Assert.Inconclusive("Verify the correctness of this test method.");
        }

        /// <summary>
        ///A test for VehicleSelector Constructor
        ///</summary>
        [Test]
        public void VehicleSelectorConstructorTest() {
            IWebDriver driver = null; // TODO: Initialize to an appropriate value
            VehicleSelector target = new VehicleSelector(driver);
            Assert.Inconclusive("TODO: Implement code to verify target");
        }
    }
}
