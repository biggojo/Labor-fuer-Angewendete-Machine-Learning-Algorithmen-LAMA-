#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <Python.h>


#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))


double
calculate_iou(double lama_rect_x, double lama_rect_y, double lama_rect_w, double lama_rect_h,
              double reference_x, double reference_y, double reference_w, double reference_h)
{
    double intersection_over_union = 0.0f;

    double xA = MAX(lama_rect_x, reference_x);
    double yA = MAX(lama_rect_y, reference_y);
    double xB = MIN(lama_rect_x + lama_rect_w, reference_x + reference_w);
    double yB = MIN(lama_rect_y + lama_rect_h, reference_y + reference_h);

    if ((xB < xA) || (yB < yA))
         return 0.0f;

    double interArea = (xB - xA) * (yB - yA);
    double lamaArea = lama_rect_w * lama_rect_h;
    double referenceArea = reference_w * reference_h;

    intersection_over_union = interArea / (lamaArea + referenceArea - interArea);

    return intersection_over_union;
}


static PyObject *
_calculate_iou( PyObject *self, PyObject *args )
{
    double lama1_rect_x; double lama1_rect_y; double lama1_rect_w; double lama1_rect_h;
    double lama2_rect_x; double lama2_rect_y; double lama2_rect_w; double lama2_rect_h;
    double lama3_rect_x; double lama3_rect_y; double lama3_rect_w; double lama3_rect_h;

    double return_value;

    if (!PyArg_ParseTuple(args, "dddddddddddd",
            &lama1_rect_x, &lama1_rect_y, &lama1_rect_w, &lama1_rect_h,
            &lama2_rect_x, &lama2_rect_y, &lama2_rect_w, &lama2_rect_h,
            &lama3_rect_x, &lama3_rect_y, &lama3_rect_w, &lama3_rect_h)) {
        return NULL;
    }

    return_value  = calculate_iou(lama1_rect_x, lama1_rect_y, lama1_rect_w, lama1_rect_h,
                                           100,          100,          300,          320);
    return_value += calculate_iou(lama2_rect_x, lama2_rect_y, lama2_rect_w, lama2_rect_h,
                                           280,          600,          250,          310);
    return_value += calculate_iou(lama3_rect_x, lama3_rect_y, lama3_rect_w, lama3_rect_h,
                                           630,          320,          300,          320);

    return Py_BuildValue("d", return_value);
}

static PyMethodDef lama_black_box_methods[] = {
   { "calculate", _calculate_iou, METH_VARARGS, NULL },
   { NULL, NULL, 0, NULL }
};

static struct PyModuleDef black_box_module = {
    PyModuleDef_HEAD_INIT,
    "lama_blackbox",  /* name of module */
    NULL,        /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
    lama_black_box_methods
};

PyMODINIT_FUNC
PyInit_lama_blackbox(void)
{
    PyObject *m;

    // (void) Py_InitModule("blackbox", black_box_methods);
    //Py_InitModule3("_black_box", black_box_methods, "docstring...");
    m = PyModule_Create(&black_box_module);
    if (m == NULL)
        return NULL;

    return m;
}

