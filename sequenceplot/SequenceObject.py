#!/usr/bin/env python
# Copyright 2012 Yummy Melon Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Charles Y. Choi
import sys

class SequenceObject:
    """
    Base class representation of a participant object in a UML sequence diagram.
    
    """
    def __init__(self, label=None):
        """
        Class constructor.

        Args:
        label -- full label of the sequence object. Typical value is 'object_name: class_name'.

        """
        self.label = label
        self.parent = None
        self.activeCount = 0
        
    def active(self):
        """
        Changes the object's status to active, and changes its
        lifeline drawing style correspondingly. An active call in an
        already active object will result in a swimlane showing a
        nested object activation.

        Corresponding UMLGraph operation:
            active(object);
        
        """
        self.activeCount = self.activeCount + 1
        buf = 'active({0});'.format(self.picName())
        self.parent.addTransaction(buf)

        
    def inactive(self):
        """
        Changes the object's status to inactive, and changes its
        lifeline drawing style correspondingly. An inactive call on a
        nested object invocation will result in showing a simple
        active swimlane.
        
        Corresponding UMLGraph operation:
            inactive(object);

        
        """
        if self.activeCount > 0:
            buf = 'inactive({0});'.format(self.picName())
            self.parent.addTransaction(buf)
            self.activeCount = self.activeCount - 1

    def delete(self):
        """
        The object deletes itself, drawing an X at the end of its
        lifeline. The object's lifeline need not be otherwise
        completed.

        Corresponding UMLGraph operation:
            delete(object);

        
        """
        buf = 'delete({0});'.format(self.picName())
        self.parent.addTransaction(buf)

        
    def cmessage(self, target, targetLabel):
        """
        Has from_object create the to_object, labeled with
        object_label. The message is labeled with the <<create>>
        stereotype.

        Corresponding UMLGraph operation:
            create_message(from_object,to_object,object_label);
        
        """
        target.label = targetLabel
        template = 'cmessage({0},{1},"{2}");'
        buf = template.format(self.picName(),
                              target.picName(),
                              targetLabel)
        
        self.parent.addTransaction(buf)

    def dmessage(self, target):
        """
        Sends a message labeled with the <<destroy>> stereotype from the
        from_object to the to_object. The object to_object is marked
        as destroyed, with an X at the end of its lifeline. The
        object's lifeline need not be otherwise completed.

        Corresponding UMLGraph operation:
            destroy_message(from_object,to_object);
            
        """
        template = 'dmessage({0},{1});'
        
        buf = template.format(self.picName(),
                              target.picName())
        
        self.parent.addTransaction(buf)

    def message(self, target, request):
        """
        Draws a message between two objects, with the given
        label. Self messages (where an objects sends a message to
        itself) are supported.

        Corresponding UMLGraph operation:
            message(from_object,to_object,label)
        
        """
        template = 'message({0},{1},"{2}");'
        
        buf = template.format(self.picName(),
                              target.picName(),
                              request)
        
        self.parent.addTransaction(buf)
        



    def rmessage(self, target, response):
        """
        Draws a return message between two objects, with the given
        label. Can also be written as rmessage.

        Corresponding UMLGraph operation:
            return_message(from_object,to_object,label)
        
        """
        template = 'rmessage({0},{1},"{2}");'

        buf = template.format(self.picName(),
                              target.picName(),
                              response)

        self.parent.addTransaction(buf)


    #
    def pushMethod(self, target, request):
        self.parent.step(1)
        target.active()
        self.parent.sync()
        self.message(target, request)
        self.parent.async()

    def popMethod(self, target, response):
        target.rmessage(self, response)
        target.inactive()
        self.parent.step(1)
        
        
    def callMethod(self, target, request, response=None, steps=0):

        self.parent.step(1)
        target.active()

        self.parent.sync()
        self.message(target, request)
        self.parent.async()
        
        if response:
            if steps:
                self.parent.step(steps)
            target.rmessage(self, response)

        target.inactive()
        self.parent.step(1)


    def createInstance(self, target, instanceName):
        self.parent.sync()
        self.cmessage(target, instanceName)
        self.parent.async()

    def destroyInstance(self, target):
        self.parent.sync()
        self.dmessage(target)
        self.parent.async()
        

    def picObjectInit(self):
        """
        Defines an object with the given name, labeled on the diagram as specified.

        Corresponding UMLGraph operation:
            object(name, label);
        
        """
        template = 'object({0},"{1}");'

        buf = template.format(self.picName(),
                              self.label)

        self.parent.addTransaction(buf)


    def picName(self):
        """
        Generates UMLGraph pic name based on python id of the instance of
        this object.
        
        """
        result = 'O_{0}'.format(id(self))
        return result


    def complete(self):
        """
        Completes the lifeline of a given object (or actor) by drawing
        its lifeline to the bottom of the diagram.

        Corresponding UMLGraph operation:
            complete(name);
        
        """
        template = 'complete({0});'
                
        buf = template.format(self.picName())
        self.parent.addTransaction(buf)


    def lconstraint(self, label):
        """
        Displays a constraint label (typically given inside curly
        braces) for the given object. The constraint will appear on
        the right of the object's lifeline at the time it appears. Can
        also be used to place an message label on the left of a
        message arrow, rather than its center. Can also be written as
        lconstraint.

        Corresponding UMLGraph operation:
            lconstraint(object,label);
        
        """
        template = 'lconstraint({0},"{1}");'
        buf = template.format(self.picName(),
                              label)
        self.addTransaction(buf)


    def lconstraintBelow(self, label):
        """
        same as lconstraint, but it will be shown below the current line instead of above.

        Corresponding UMLGraph operation:
            lconstraint_below(object,label);
        
        """

        template = 'lconstraint_below({0},"{1}");'
        buf = template.format(self.picName(),
                              label)
        self.addTransaction(buf)
        
