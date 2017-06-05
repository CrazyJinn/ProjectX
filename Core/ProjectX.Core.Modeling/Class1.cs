using System.Collections.Generic;
using ProjectX.Core.Model;

namespace ProjectX.Core.Modeling
{
    public class Class1
    {
        public List<Input> GetInput()
        {
            var inputList = new List<Input>();
            var inputA = new Input()
            {

                ResultList = new List<int>()
                {
                    2,4,6,
                },
                ParameterList = new List<Parameter>()
                {
                    new Parameter()
                    {
                        ParameterName="X",
                        ParameterValueList = new List<int>()
                        {
                            1,2,3,
                        }
                    },
                    new Parameter()
                    {
                        ParameterName="Y",
                        ParameterValueList = new List<int>()
                        {
                            1,2,3,
                        }
                    },
                },
            };
            var inputB = new Input()
            {

                ResultList = new List<int>()
                {
                    3,6,9,
                },
                ParameterList = new List<Parameter>()
                {
                    new Parameter()
                    {
                        ParameterName="X",
                        ParameterValueList = new List<int>()
                        {
                            1,2,3,
                        }
                    },
                    new Parameter()
                    {
                        ParameterName="Y",
                        ParameterValueList = new List<int>()
                        {
                            2,4,6,
                        }
                    },
                },
            };
            inputList.Add(inputA);
            inputList.Add(inputB);
            return inputList;
        }

    }
}
